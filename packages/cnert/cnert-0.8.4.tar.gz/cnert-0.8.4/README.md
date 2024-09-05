# cnert

[![PyPI version](https://badge.fury.io/py/cnert.svg)](https://badge.fury.io/py/cnert)
[![Documentation Status](https://readthedocs.org/projects/cnert/badge/?version=latest)](https://cnert.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/maartenq/cnert/main.svg)](https://results.pre-commit.ci/latest/github/maartenq/cnert/main)
[![workflow ci](https://github.com/maartenq/cnert/actions/workflows/main.yml/badge.svg)](https://github.com/maartenq/cnert/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/maartenq/cnert/branch/main/graph/badge.svg?token=XXXXXXXXXX)](https://codecov.io/gh/maartenq/cnert)
[![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue.svg)](LICENSE)


# Cnert - TLS Certificates for testing

Cnert is simple Python API for creating TLS Certificates and stuff for testing
purposes (on top of [cryptography]).

[cnert.CA][] makes it easy to create CAs, intermediate CAs. These CA objects
can then issue directly [certificates][cnert._Cert].

Cnert can make CSRs. CA objects also use these to issue certificates.

Subject and Issuer Name Attributes, Subject Alternative Names, not_before_date
and not_after_data can all be set.

Cnert has different methods to introspect these.

Cnert is made specially made for testing application that *do something* with
TLS certificate and there for can make tailor made certificates for testing
those apps.

If you don't need that and you just need any "old" certificate, you probably
better of with [trustme], trust me, or better: trust them.


## Usage

### Create a root CA

    >>> import cnert
    >>> ca = cnert.CA()

    >>> ca.is_root_ca
    True

    >>> ca.is_intermediate_ca
    False

    >>> ca.parent is None
    True


### Issue an intermediate CA

    >>> intermediate = ca.issue_intermediate()
    >>> intermediate.is_intermediate_ca
    True

    >>> intermediate.is_root_ca
    False

    >>> intermediate.parent is ca
    True


###  Inspect the CA's certificate

    >>> ca.cert
    <cnert.Cert at 0x112a14c50>

    >>> ca.cert.subject_attrs
    NameAttrs(ORGANIZATION_NAME="Root CA")

    >>> ca.cert.subject_attrs.dict_
    {'ORGANIZATION_NAME': 'Root CA'}

    >>> ca.cert.subject_attrs.ORGANIZATION_NAME
    'Root CA'

    >>> ca.cert.ca.cert.issuer_attrs
    NameAttrs(ORGANIZATION_NAME="Root CA")

    >>> ca.cert.not_valid_before
    datetime.datetime(2023, 3, 24, 21, 27, 50, 579389

    >>> ca.cert.not_valid_after
    datetime.datetime(2023, 6, 23, 20, 20, 47, 999034)

    >>> ca.cert.not_valid_after
    datetime.datetime(2023, 6, 23, 20, 20, 47, 999034)

    >>> ca.cert.serial_number
    710111479237500376112637726504312543434663217892

    >>> ca.cert.path_length
    9

    >>> ca.cert.public_key.key_size
    2048

    >>> ca.cert.pem
    b'-----BEGIN CERTIFICATE-----\nMIIC9zCCAd+gAwIBAgIUGyCBgdyVPVGlYIJj25+x1AMQPHswDQYJKoZIhvcNAQEL\nBQAwEjEQMA4GA1UECgwHUm9vdCBDQTAeFw0yMzA1MDgwODQyNThaFw0yMzA4MDcw\nODQyNThaMBIxEDAOBgNVBAoMB1Jvb3QgQ0EwggEiMA0GCSqGSIb3DQEBAQUAA4IB\nDwAwggEKAoIBAQDK13Q6dZdK17SPmplwTq4Phh7TatM4HQqONEq6+xE2VnJ9eeCh\nQYM5w5dnxIUeV10j3ODPJz5L+6IirV/e6voCWkS6Vgzh/lAVTbUVGANR26NpMnjm\n/qU0NUYuSQo5QFJuwFEx9CZ1xGTac9gspBo1jO7E9m01pRAXlr1HqTZT7mY4LNWb\nDyjKmMa/tfK0+itiKce48hZDxqy3YLnWYyIAZ+rTrf9RW5hpLb6g/KeAf3w5q55Q\nL2dCsC6flZ6NFVRm7okpawwN2tf5c451fMm3B+GtVJJMP+6lmk6MC3h++pcwOimg\nUwB8tYEPoZHuMjd1hacZcbfGFzCGAbme+BZbAgMBAAGjRTBDMB0GA1UdDgQWBBSA\nIsRH6giY94MEfhzafTd5WC2HMzASBgNVHRMBAf8ECDAGAQH/AgEJMA4GA1UdDwEB\n/wQEAwIBpjANBgkqhkiG9w0BAQsFAAOCAQEACLdxWMlmr3drMvA7GaQArzlbe/ny\nx8mThDhZP6gx+yTJ6LXk8CFc7S23JXFZVquwcV5yFa0DavaodBI3RNWknx/Yu5Lm\nM7cOByu2IuJhcEu4o+ZntLZLb7heFMXMIf01lVkYpyYyvS/NvVdu9km8f6ZvxV9r\nDyTDDMjeh+hg5l2Wwc4P6UGoMlmOruUiunsb8hiDLhD+brYBHKHqJY9pCrzJQd0v\nWEkAOsBwaTv/POO0F4VDZSfA5CqjYOkppupw9nXXfJkk9PvKuDI1G2XO7pcW1PWh\nDdGK6Wz0AXMWWbbX8LToDrFA9q7YOxGNOVPhbHZ++bDJvLNmjrtruy3UTQ==\n-----END CERTIFICATE-----\n'


###  Inspect the Intermediate CA

    >>> intermediate.cert.subject_attrs
    NameAttrs(ORGANIZATION_NAME="CA Intermediate 1")

    >>> intermediate.cert.ca.cert.issuer_attrs
    NameAttrs(ORGANIZATION_NAME="Root CA")

    >>> intermediate.cert.path_length
    8


###  Issue a cert from a CA (without CSR)
    >>> cert = ca.issue_cert()

    >>> cert.subject_attrs
    NameAttrs(COMMON_NAME="example.com")

    >>> cert.subject_attrs.dict_
    {'COMMON_NAME': 'example.com'}

    >>> cert.subject_attrs.COMMON_NAME
    'example.com'

    >>> cert.public_key
    <cryptography.hazmat.backends.openssl.rsa._RSAPublicKey object at 0x10361c150>

    >>> cert.pem
    b'-----BEGIN CERTIFICATE-----\nMIIDITCCAgmgAwIBAgIUAx6AA8z3BqH/ICCmqOJXGI7PHCswDQYJKoZIhvcNAQEL\nBQAwEjEQMA4GA1UECgwHUm9vdCBDQTAeFw0yMzA1MDgwODU5NTlaFw0yMzA4MDcw\nODU5NTlaMBYxFDASBgNVBAMMC2V4YW1wbGUuY29tMIIBIjANBgkqhkiG9w0BAQEF\nAAOCAQ8AMIIBCgKCAQEAnWAlLvbR0hE8seqI8uBj8ESicJ/nF8I3KF9CFlTexQ73\nKdyqTRCoPZ6uuK0quX+qX5KeeNlWSnJRxSDc0WmLwYxWFVg6hmBDPLK1Ijntc1Uj\n4HENkolgPUBxgf9VBSmojqd1XL0o8PwGFIoyZ6Z/YTc3MqML4QZaB0m+TYlVgoJP\nQgFT9d9nQadvyswIx7nOMkT0Rd3sGl8nWaNgDaBLB6mkylGrtaiyo2M2LWKvNz69\nDWbjlccj65B04cBLwRcA2Zmx80leajX1zNWt0+dhJFo6rnLtmvIgqdLhCrNTmDMK\nrlyVsOrwJfXNreIPDEgYztZlrUdTnynmF4bW6W5KcwIDAQABo2swaTAdBgNVHQ4E\nFgQURd1r0d7XJBtT651AbuR2hg7TQBIwDAYDVR0TAQH/BAIwADAOBgNVHQ8BAf8E\nBAMCBaAwKgYDVR0lAQH/BCAwHgYIKwYBBQUHAwIGCCsGAQUFBwMBBggrBgEFBQcD\nAzANBgkqhkiG9w0BAQsFAAOCAQEANcFmZZkt4Z6jc069IOonGfcpUdnZieSEVyBE\nCQC+QWaHYqcD0ryYV8n1/UzNVcSkptQ5YrbgXNikV6+cuklFq4OjHlUDGOxchrkc\nSFGYAf+j7wAAx+OZWH5IwvMSTWGhfi7FWNFrzbO3JUE1q3OOnsIUmcDpd/8zucyE\njPf6F0MVujwMJq8VAH8UtUpVm1SApEBz9vgx0n7Z0l5fgRw7PMwwDkaoyplSC0VA\n7F7AUX3K0oJ7Gyw+9onfS090GMo6mlTfhtXNpPArleUUOTrp+TKVhwtz8GRRzxEW\nBE1OaNZaipKILZPbgDa5u67pRdU/OhuMFDsBh1GlPopcax+rCQ==\n-----END CERTIFICATE-----\n'

    >>> cert.SHA1
    '21B99CE5588417932ACB65C54398115C75240B04'


###  Issue a cert from a CA with alt names

    >>> cert = ca.issue_cert("www.example.com", "host1.example.com", "example.com")

    >>> cert.subject_attrs
    NameAttrs(COMMON_NAME="www.example.com")

    >>> cert.sans
    ('www.example.com', 'host1.example.com', 'example.com')

    >>> cert.certificate.extensions[4]
    <Extension(oid=<ObjectIdentifier(oid=2.5.29.17, name=subjectAltName)>, critical=True, value=<SubjectAlte rnativeName(<GeneralNames([<DNSName(value='www.example.com')>, <DNSName(value='host1.example.com')>, <DNSName(val ue='example.com')>])>)>)>

###  Create a CSR

    >>> csr = cnert.CSR()

    >>> csr.pem
    b'-----BEGIN CERTIFICATE REQUEST-----\nMIICWzCCAUMCAQAwFjEUMBIGA1UEAwwLZXhhbXBsZS5jb20wggEiMA0GCSqGS
    Ib3\nDQEBAQUAA4IBDwAwggEKAoIBAQCzMgKx18z/G6WFc7ULVZS8gEHYW7jNmBM0wvIG\nCFkGu8UzPZL/dHpb4UAAA3kJ+MpYUYvjAuLxoh
    6RarbkfChGSGvrJVzbNJtj0axL\n3ryyZ4WhSPFGQnLCze/CsnZbZV+a2B6kdnpb2xge+pa8owGSp3jQRlqFy03tBhAK\nrXlQ/XNQ9xN7CDM
    8tHyPwJtl2wHegg7zHI/pjGGoXxfz1E6257+lgIL8lIooRpgu\nXPTp/ZCBumBlNjTtITcL8AUFuRfEAXvLRjVFXh4oOBBddQUNvGwKBUZDqC
    zNoxRz\ntcd4ZeWL3BrwkRsKZ6gnV3rxhoIk3Bysf2ckeE1kKIdHQ+jHAgMBAAGgADANBgkq\nhkiG9w0BAQsFAAOCAQEAcintXa9ErBuCNw8
    pNftb3ENKMC7+AhNQ6wchBvTZw6Kp\nA30kV/LEjSHSGoL1rNYweUqA2NXyKT3Nm8ey4cfgpqc1L+NQfO65Hbf+PODwgIcr\nAB5fW7xZwei/
    weCoxYoznknv/9UN9IHT/3itFCO6XYdW7+TbbZ2Hfqo/fZHadZpQ\ntCndu3zTyEZfa2uw2OXapDgfpI16WiF1MGEf67b+8WoXfGW/bbzTfRy
    qX4tfqS2I\nRATog8sQheC1zhh9LTGRYFSqEd15RPIDuXcc902YEXQrbniVF2TwV/qtKqqqcvZu\nPsOCzwRJq87N39XWH1EInVFfftHOTWn9
    HatP/+RbrQ==\n-----END CERTIFICATE REQUEST-----\n'

    >>> csr.subject_attrs.COMMON_NAME
    'example.com'

[cryptography]: https://cryptography.io/en/latest/
[trustme]: https://github.com/python-trio/trustme


[cnert.CA]: https://cnert.readthedocs.io/en/latest/cnert/#class-cnertca
[cnert._Cert]: https://cnert.readthedocs.io/en/latest/cnert/#class-cnert_cert
