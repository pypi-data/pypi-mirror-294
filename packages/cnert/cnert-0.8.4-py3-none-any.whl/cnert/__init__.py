# cnert/__init__.py

from __future__ import annotations  # for Python 3.7-3.9

import datetime
from ipaddress import ip_address, ip_network
from typing import ClassVar

import idna
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

"""
Cnert makes TLS private keys, CSRs, private CAs and certificates.
"""

__version__ = "0.8.3"
__title__ = "Cnert"
__description__ = (
    "Cnert makes TLS private keys, CSRs, private CAs and certificates."
)
__uri__ = "https://github.com/maartenq/cnert"
__author__ = "Maarten"
__email__ = "ikmaarten@gmail.com"
__license__ = "MIT or Apache License, Version 2.0"
__copyright__ = "Copyright (c) 2023  Maarten"


def build_private_key(
    key_size: int = 2048,
    public_exponent: int = 65537,
) -> rsa.RSAPrivateKey:
    """
    Creates a private key.

    Parameters:
        key_size: Key size
        public_exponent: public exponenent
    """
    return rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
        backend=default_backend(),
    )


def idna_encode(_string: str) -> str:
    """
    Creates a valid  internationalized domain name

    Parameters:
        _string: Internationalized domain name
    """
    for prefix in ["*.", "."]:
        if _string.startswith(prefix):
            _string = _string[len(prefix) :]
            _bytes = prefix.encode("ascii") + idna.encode(_string, uts46=True)
            return _bytes.decode("ascii")
    return idna.encode(_string, uts46=True).decode("ascii")


def identity_string_to_x509(identity: str) -> x509.GeneralName:
    """
    Creates a x509.GeneralName from a string.

    Parameters:
        identity: IP Address, DNS name or email address.
    """
    try:
        return x509.IPAddress(ip_address(identity))
    except ValueError:
        try:
            return x509.IPAddress(ip_network(identity))
        except ValueError:
            if "@" in identity:
                return x509.RFC822Name(identity)
            return x509.DNSName(idna_encode(identity))


class Freezer:
    """
    Freeze any class such that instantiated objects become immutable.
    """

    __slots__: ClassVar[list[str]] = []
    _frozen: bool = False

    def __init__(self):
        for attr_name in dir(self):
            self.__slots__.append(attr_name)
        self._frozen = True

    def __delattr__(self, *args, **kwargs):
        if self._frozen:
            raise AttributeError("This object is frozen!")
        object.__delattr__(self, *args, **kwargs)

    def __setattr__(self, *args, **kwargs):
        if self._frozen:
            raise AttributeError("This object is frozen!")
        object.__setattr__(self, *args, **kwargs)


class NameAttrs(Freezer):
    """
    An object for storing (and freezing) Name Attributes for Subject Name
    Attributes and Issuer Name Attributes.

    Accepts any valid x509.NameAttribute as key arguments with arbitrary string
    values.

    Has methods for returning initialized attributes in a dict and for
    returning a `cryptography.x509.Name`

    There is alse a method for showing the allowed attributes.

    Examples:
        >>> subject_attrs = cnert.NameAttrs(COMMON_NAME="example.com")
        >>> subject_attrs.COMMON_NAME
        'example.com'
        >>> subject_attrs.dict_
        {'COMMON_NAME': 'example.com'}
        >>> subject_attrs.x509_name
        <Name(CN=example.com)>
    """

    BUSINESS_CATEGORY: str
    COMMON_NAME: str
    COUNTRY_NAME: str
    DN_QUALIFIER: str
    DOMAIN_COMPONENT: str
    EMAIL_ADDRESS: str
    GENERATION_QUALIFIER: str
    GIVEN_NAME: str
    INN: str
    JURISDICTION_COUNTRY_NAME: str
    JURISDICTION_LOCALITY_NAME: str
    JURISDICTION_STATE_OR_PROVINCE_NAME: str
    LOCALITY_NAME: str
    OGRN: str
    ORGANIZATIONAL_UNIT_NAME: str
    ORGANIZATION_NAME: str
    POSTAL_ADDRESS: str
    POSTAL_CODE: str
    PSEUDONYM: str
    SERIAL_NUMBER: str
    SNILS: str
    STATE_OR_PROVINCE_NAME: str
    STREET_ADDRESS: str
    SURNAME: str
    TITLE: str
    UNSTRUCTURED_NAME: str
    USER_ID: str
    X500_UNIQUE_IDENTIFIER: str

    def __init__(self, **kwargs) -> None:
        self._name_oids: list[x509.NameAttribute] = []
        self.dict_: dict[str, str] = {}
        keys = list(kwargs.keys())
        keys.sort()
        for key in keys:
            self._name_oids.append(
                x509.NameAttribute(getattr(NameOID, key), kwargs[key])
            )
            setattr(self, key, kwargs[key])
            self.dict_[key] = kwargs[key]
        super().__init__()

    def x509_name(self) -> x509.Name:
        """
        Examples:
            >>> subject_attrs = cnert.NameAttrs(COMMON_NAME="example.com")
            >>> subject_attrs.x509_name()
            <Name(CN=example.com)>

        Returns:
            A `cryptography.x509.Name`
        """
        return x509.Name(self._name_oids)

    def allowed_keys(self) -> list[str]:
        """
        Returns a list of allowed key arguments.

        Examples:
            >>> cnert.NameAttrs().allowed_keys()
            ['BUSINESS_CATEGORY',
             'COMMON_NAME',
             'COUNTRY_NAME',
             'DN_QUALIFIER',
             'DOMAIN_COMPONENT',
             'EMAIL_ADDRESS',
             'GENERATION_QUALIFIER',
             'GIVEN_NAME',
             'INN',
             'JURISDICTION_COUNTRY_NAME',
             'JURISDICTION_LOCALITY_NAME',
             'JURISDICTION_STATE_OR_PROVINCE_NAME',
             'LOCALITY_NAME',
             'OGRN',
             'ORGANIZATIONAL_UNIT_NAME',
             'ORGANIZATION_NAME',
             'POSTAL_ADDRESS',
             'POSTAL_CODE',
             'PSEUDONYM',
             'SERIAL_NUMBER',
             'SNILS',
             'STATE_OR_PROVINCE_NAME',
             'STREET_ADDRESS',
             'SURNAME',
             'TITLE',
             'UNSTRUCTURED_NAME',
             'USER_ID',
             'X500_UNIQUE_IDENTIFIER']

        Returns:
            A list of valid key attributes.
        """
        return sorted(self.__class__.__dict__["__annotations__"].keys())

    def __eq__(self, other) -> bool:
        return self.dict_ == other.dict_

    def __str__(self) -> str:
        return self.x509_name().rfc4514_string()

    def __repr__(self) -> str:
        args = ", ".join(f'{x[0]}="{x[1]}"' for x in self.dict_.items())
        return f"NameAttrs({args})"


class _CertBuilder:
    """
    Builds and signs a X509 Certificate.
    """

    def __init__(self) -> None:
        self.builder = x509.CertificateBuilder()

    @staticmethod
    def _key_usage(
        content_commitment: bool = False,
        crl_sign: bool = False,
        data_encipherment: bool = False,
        decipher_only: bool = False,
        digital_signature: bool = True,
        encipher_only: bool = False,
        key_agreement: bool = False,
        key_cert_sign: bool = False,
        key_encipherment: bool = True,
    ) -> x509.KeyUsage:
        """
        Create X509.KeyUsage objects.
        """
        return x509.KeyUsage(
            content_commitment=content_commitment,
            crl_sign=crl_sign,
            data_encipherment=data_encipherment,
            decipher_only=decipher_only,
            digital_signature=digital_signature,
            encipher_only=encipher_only,
            key_agreement=key_agreement,
            key_cert_sign=key_cert_sign,
            key_encipherment=key_encipherment,
        )

    def _add_ca_extension(self) -> None:
        """
        Add CA extension.
        """
        self.builder = self.builder.add_extension(
            self._key_usage(
                digital_signature=True,
                key_cert_sign=True,
                crl_sign=True,
            ),
            critical=True,
        )

    def _add_leaf_cert_extension(self) -> None:
        """
        Add leaf extension.
        """
        self.builder = self.builder.add_extension(
            self._key_usage(),
            critical=True,
        ).add_extension(
            x509.ExtendedKeyUsage(
                [
                    ExtendedKeyUsageOID.CLIENT_AUTH,
                    ExtendedKeyUsageOID.SERVER_AUTH,
                    ExtendedKeyUsageOID.CODE_SIGNING,
                ]
            ),
            critical=True,
        )

    def _add_subject_alt_name_extension(self, *sans: str) -> None:
        """
        Add Subject Alternative Name extension.

        Parameters:
            sans: Subject Alternative Names as positional arguments.
        """
        self.builder = self.builder.add_extension(
            x509.SubjectAlternativeName(
                [identity_string_to_x509(san) for san in sans]
            ),
            critical=True,
        )

    def _add_authority_key_identifier_extension(
        self,
        issuer_public_key: rsa.RSAPublicKey,
    ) -> None:
        """
        Add Authority Key Identifier extension.

        Parameters:
            issuer_public_key: Issuer Public key
        """
        self.builder = self.builder.add_extension(
            x509.AuthorityKeyIdentifier.from_issuer_public_key(
                issuer_public_key
            ),
            critical=False,
        )

    def build(
        self,
        sans: tuple[()] | tuple[str, ...],
        subject_attrs_X509_name: x509.Name,
        issuer_attrs_X509_name: x509.Name,
        serial_number: int,
        not_valid_before: datetime.datetime,
        not_valid_after: datetime.datetime,
        is_ca: bool,
        public_key: rsa.RSAPublicKey,
        issuer_public_key: rsa.RSAPublicKey | None = None,
        path_length: int | None = None,
    ) -> None:
        """
        Does the Certificate building.

        Parameters:
            sans: Subject Alternative Names as positional arguments.
            subject_attrs_X509_name: Subject Attributes Names.
            issuer_attrs_X509_name: Issuer Atributes Names.
            serial_number: Serial number.
            not_valid_before: Not valid before date.
            not_valid_after: Note valid after date.
            is_ca: Add CA extension.
            public_key: Public key for the certificate.
            issuer_public_key: Issuer public key.
            path_length: Max path length.
        """
        self.builder = (
            self.builder.subject_name(subject_attrs_X509_name)
            .issuer_name(issuer_attrs_X509_name)
            .public_key(public_key)
            .serial_number(serial_number)
            .not_valid_before(not_valid_before)
            .not_valid_after(not_valid_after)
            .add_extension(
                x509.SubjectKeyIdentifier.from_public_key(public_key),
                critical=False,
            )
            .add_extension(
                x509.BasicConstraints(
                    ca=is_ca,
                    path_length=path_length,
                ),
                critical=True,
            )
        )
        if issuer_public_key is not None:
            self._add_authority_key_identifier_extension(issuer_public_key)
        if is_ca:
            self._add_ca_extension()
        else:
            self._add_leaf_cert_extension()
        if sans:
            self._add_subject_alt_name_extension(*sans)

    def sign(self, private_key: rsa.RSAPrivateKey) -> x509.Certificate:
        return self.builder.sign(
            private_key=private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend(),
        )


class _Cert:
    """
    A _Cert object.

    This object is returned by [`cnert.CA().issue_cert()`][cnert.CA.issue_cert]

    Examples:

        >>> ca = CA()
        >>> cert = ca.issue_cert()
        >>> cert.subject_attrs
        NameAttrs(COMMON_NAME="example.com")
        >>> cert.issuer_attrs
        NameAttrs(ORGANIZATION_NAME="Root CA")
        >>> cert.not_valid_before
        datetime.datetime(2023, 3, 24, 23, 56, 55, 901545)
        >>> cert.not_valid_after
        datetime.datetime(2023, 6, 23, 23, 56, 55, 901545)
    """

    def __init__(
        self,
        *sans: str,
        subject_attrs: NameAttrs,
        issuer_attrs: NameAttrs,
        not_valid_before: datetime.datetime | None = None,
        not_valid_after: datetime.datetime | None = None,
        serial_number: int | None = None,
        parent: _Cert | None = None,
        private_key: rsa.RSAPrivateKey | None = None,
        path_length: int = 0,
        is_ca: bool = False,
    ) -> None:
        """
        Initialize a _Cert object.

        Parameters:
            sans: Subject Alternative Names as positional arguments
            subject_attrs: Subject Name Attributes
            issuer_attrs: Issure Name Attributes
            not_valid_before: CA not valid before date
            not_valid_after: CA not valid after date
            serial_number: Serial number
            parent: Certificate of CA.
            private_key: RSA private key
            path_length: Path length
            is_ca: if CA
        """
        if not_valid_before is None:
            not_valid_before = datetime.datetime.now(datetime.timezone.utc)

        if not_valid_after is None:
            not_valid_after = not_valid_before + datetime.timedelta(weeks=13)

        if serial_number is None:
            serial_number = x509.random_serial_number()

        if private_key is None:
            self.private_key = build_private_key()
        else:
            self.private_key = private_key

        self.sans = sans
        self.subject_attrs = subject_attrs
        self.issuer_attrs = issuer_attrs
        self.parent = parent
        self.not_valid_before = not_valid_before
        self.not_valid_after = not_valid_after
        self.serial_number = serial_number
        self.path_length = path_length
        self.is_ca = is_ca
        self._build_certificate()

    def _build_certificate(self):
        cert_builder = _CertBuilder()
        cert_builder.build(
            sans=self.sans,
            subject_attrs_X509_name=self.subject_attrs.x509_name(),
            issuer_attrs_X509_name=self.issuer_attrs.x509_name(),
            serial_number=self.serial_number,
            not_valid_before=self.not_valid_before,
            not_valid_after=self.not_valid_after,
            is_ca=self.is_ca,
            public_key=self.public_key,
            issuer_public_key=(
                self.parent.public_key if self.parent else None
            ),
            path_length=None if not self.is_ca else self.path_length,
        )
        self.certificate = cert_builder.sign(
            self.parent.private_key if self.parent else self.private_key,
        )
        self.pem = self.certificate.public_bytes(serialization.Encoding.PEM)

    @property
    def private_key_pem_PKCS1(self) -> bytes:
        """
        Examples:
            >>> cert = CA().issue_cert()
            >>> cert.private_key_pem_PKCS1
            b'-----begin rsa private key-----
            ...


        Returns:
            PEM encoded serialized key in TraditionalOpenSSL format.
        """
        return self.private_key.private_bytes(
            serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def private_key_pem_PKCS8(self) -> bytes:
        """
        Examples:
            >>> cert = CA().issue_cert()
            >>> cert.private_key_pem_PKCS8
            b'-----BEGIN PRIVATE KEY-----
            ...

        Returns:
            PEM encoded serialized key in PKCS8 format.
        """
        return self.private_key.private_bytes(
            serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def public_key(self) -> rsa.RSAPublicKey:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.private_key
            <cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey object
            at 0x1014e4e10>

        Returns:
            An RSA private key.
        """
        return self.private_key.public_key()

    @property
    def public_key_pem(self) -> bytes:
        """
        Examples:
            >>> cert = CA().issue_cert()
            >>> cert.public_key_pem
            b'-----BEGIN PUBLIC KEY-----
            ...


        Returns:
            PEM encoded serialized key in RSAPublicKey format.
        """
        return self.public_key.public_bytes(
            serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    @property
    def MD5(self) -> str:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.MD5
            'A03D37486DD47BE3E9C7EC1624073856'

        Returns:
            MD5 Fingerprint string in hexadecimal and upper case.
        """
        return bytes.hex(
            self.certificate.fingerprint(hashes.MD5()),  # noqa: S303
        ).upper()

    @property
    def SHA1(self) -> str:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.SHA1
            '9E0A06CFB37B352FDA5B2226E6D631CF07D5D185'

        Returns:
            SHA1 Fingerprint string in hexadecimal and upper case.
        """
        return bytes.hex(
            self.certificate.fingerprint(hashes.SHA1()),  # noqa: S303
        ).upper()

    @property
    def SHA256(self) -> str:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.SHA256
            '68307A6CBE2804038DF85FB53AEE96AB47EA81439AB2E059DDDEA9F901097D84'

        Returns:
            SHA256 Fingerprint string in hexadecimal and upper case.
        """
        return bytes.hex(self.certificate.fingerprint(hashes.SHA256())).upper()

    @property
    def subject_key_identifier_digest(self) -> str:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.subject_key_identifier_digest
            '8F85C564F62E39D5A5CA346CA26AAE67029B671E'

        Returns:
            The binary value of the subject key identifier in hexadecimal
            and upper case.
        """
        ext = self.certificate.extensions.get_extension_for_oid(
            x509.ExtensionOID.SUBJECT_KEY_IDENTIFIER
        )
        return bytes.hex(ext.value.key_identifier).upper()

    @property
    def authority_key_identifier_digest(self) -> str | None:
        """
        Examples:
            >>> cert = cnert.CA().issue_cert()
            >>> cert.authority_key_identifier_digest
            '8F85C564F62E39D5A5CA346CA26AAE67029B671E'

        Returns:
            The binary value of the authority key identifier in hexadecimal
            and upper case or None when certificate has no
            subject key identifier extension.
        """
        try:
            ext = self.certificate.extensions.get_extension_for_oid(
                x509.ExtensionOID.AUTHORITY_KEY_IDENTIFIER
            )
            return bytes.hex(ext.value.key_identifier).upper()
        except x509.ExtensionNotFound:
            return None

    def __str__(self) -> str:
        return f"Certificate {self.subject_attrs}"


class CSR:
    """
    A CSR object.

    Examples:
        >>> csr = cnert.CSR()

    Parameters:
        sans: Subject Alternative Names as positional arguments
        subject_attrs: Subject Name Attributes
        private_key: RSA private key

    """

    def __init__(
        self,
        *sans: str,
        subject_attrs: NameAttrs | None = None,
        private_key: rsa.RSAPrivateKey | None = None,
    ) -> None:
        self.sans = sans

        if subject_attrs is None:
            if sans:
                subject_attrs = NameAttrs(COMMON_NAME=sans[0])
            else:
                subject_attrs = NameAttrs(COMMON_NAME="example.com")
        self.subject_attrs = subject_attrs

        if private_key is None:
            self.private_key = build_private_key()
        else:
            self.private_key = private_key

        self._csr_builder = (
            x509.CertificateSigningRequestBuilder().subject_name(
                subject_attrs.x509_name()
            )
        )
        self.CSR = self._gen_csr()

    def _add_subject_alt_name_extension(self) -> None:
        self._csr_builder = self._csr_builder.add_extension(
            x509.SubjectAlternativeName(
                [identity_string_to_x509(san) for san in self.sans]
            ),
            critical=False,
        )

    def _gen_csr(self) -> x509.CertificateSigningRequest:
        if self.sans:
            self._add_subject_alt_name_extension()
        csr = self._csr_builder.sign(
            private_key=self.private_key,
            algorithm=hashes.SHA256(),
            backend=default_backend(),
        )
        self.pem = csr.public_bytes(serialization.Encoding.PEM)
        return csr

    @property
    def private_key_pem_PKCS1(self) -> bytes:
        return self.private_key.private_bytes(
            serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def private_key_pem_PKCS8(self) -> bytes:
        return self.private_key.private_bytes(
            serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    @property
    def public_key(self) -> rsa.RSAPublicKey:
        return self.private_key.public_key()

    def __str__(self) -> str:
        return f"Certificate {self.subject_attrs}"


class CA:
    """
    A CA object.

    Examples:
        >>> ca = cnert.CA()
        >>> ca.is_root_ca
        True
        >>> ca.is_intermediate_ca
        False
        >>> ca.parent is None
        True

    Parameters:
        subject_attrs: Subject Name Attributes.
        subject_attrs: Issuer Name Attributes.
        path_length: Maximum path length certificates subordinate.
        not_valid_before: CA not valid before date.
        not_valid_after: CA not valid after date.
        parent: Parent of CA.
        intermediate_num: Number of intermediates.
    """

    def __init__(
        self,
        subject_attrs: NameAttrs | None = None,
        issuer_attrs: NameAttrs | None = None,
        path_length: int = 9,
        not_valid_before: datetime.datetime | None = None,
        not_valid_after: datetime.datetime | None = None,
        serial_number: int | None = None,
        parent: CA | None = None,
        intermediate_num: int = 0,
    ) -> None:
        self.intermediate_num = intermediate_num
        self.parent = parent

        if subject_attrs is None:
            subject_attrs = NameAttrs(ORGANIZATION_NAME="Root CA")

        if issuer_attrs is None:
            issuer_attrs = subject_attrs

        self.cert = _Cert(
            subject_attrs=subject_attrs,
            issuer_attrs=issuer_attrs,
            path_length=path_length,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            serial_number=serial_number,
            parent=(
                self.parent.cert  # type: ignore[has-type]
                if self.parent is not None
                else None
            ),
            is_ca=True,
        )

    def __str__(self) -> str:
        return f"CA {self.cert.subject_attrs}"

    @property
    def is_root_ca(self) -> bool:
        """
        Examples:
            >>> ca = CA()
            >>> ca.is_root_ca
            True
            >>> intermediate = ca.issue_intermediate()
            >>> intermediate.is_root_ca
            False

        Returns:
            Whether CA is a root CA or not.
        """
        return self.intermediate_num < 1

    @property
    def is_intermediate_ca(self) -> bool:
        """
        Returns:
            Whether CA is a intermediate CA or not.
        """
        return self.intermediate_num > 0

    def issue_intermediate(
        self,
        subject_attrs: NameAttrs | None = None,
        not_valid_before: datetime.datetime | None = None,
        not_valid_after: datetime.datetime | None = None,
        serial_number: int | None = None,
    ) -> CA:
        if self.cert.path_length == 0:
            raise ValueError("Can't create intermediate CA: path length is 0")
        intermediate_num = self.intermediate_num + 1
        return CA(
            subject_attrs=subject_attrs
            or NameAttrs(
                ORGANIZATION_NAME=f"CA Intermediate {intermediate_num}"
            ),
            issuer_attrs=self.cert.subject_attrs,
            path_length=self.cert.path_length - 1,
            not_valid_before=not_valid_before or self.cert.not_valid_before,
            not_valid_after=not_valid_after or self.cert.not_valid_after,
            serial_number=serial_number,
            parent=self,
            intermediate_num=intermediate_num,
        )

    def issue_cert(
        self,
        *sans: str,
        subject_attrs: NameAttrs | None = None,
        not_valid_before: datetime.datetime | None = None,
        not_valid_after: datetime.datetime | None = None,
        serial_number: int | None = None,
        csr: CSR | None = None,
    ) -> _Cert:
        """
        Issues a certificate

        Examples:
            >>> ca = CA()
            >>> ca.issue_cert()
            <cnert.Cert at 0x107f87f50>

        Parameters:
            sans: Subject Alternative Names as positional arguments.
            subject_attrs: Subject Name Attributes.
            not_valid_before: Certificate not valid before date.
            not_valid_after: Certificate not valid after date.
            csr: A CSR object.

        Returns:
            A _Cert object.

        """
        if csr:
            sans = csr.sans
            subject_attrs = csr.subject_attrs
            private_key = csr.private_key
        else:
            private_key = None
            if subject_attrs is None:
                if sans:
                    subject_attrs = NameAttrs(COMMON_NAME=sans[0])
                else:
                    subject_attrs = NameAttrs(COMMON_NAME="example.com")
        return _Cert(
            *sans,
            subject_attrs=subject_attrs,
            issuer_attrs=self.cert.subject_attrs,
            not_valid_before=not_valid_before,
            not_valid_after=not_valid_after,
            serial_number=serial_number,
            parent=self.cert,
            private_key=private_key,
        )
