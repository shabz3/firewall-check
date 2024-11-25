
PCERT_CONTEXT = POINTER(CERT_CONTEXT)
PCCERT_CONTEXT = POINTER(PCERT_CONTEXT)


class CERT_ENHKEY_USAGE(Structure):
    _fields_ = (
        ("cUsageIdentifier", DWORD),
        ("rgpszUsageIdentifier", POINTER(LPSTR)),
    )


PCERT_ENHKEY_USAGE = POINTER(CERT_ENHKEY_USAGE)


class CERT_USAGE_MATCH(Structure):
    _fields_ = (
        ("dwType", DWORD),
        ("Usage", CERT_ENHKEY_USAGE),
    )


class CERT_CHAIN_PARA(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("RequestedUsage", CERT_USAGE_MATCH),
        ("RequestedIssuancePolicy", CERT_USAGE_MATCH),
        ("dwUrlRetrievalTimeout", DWORD),
        ("fCheckRevocationFreshnessTime", BOOL),
        ("dwRevocationFreshnessTime", DWORD),
        ("pftCacheResync", LPFILETIME),
        ("pStrongSignPara", c_void_p),
        ("dwStrongSignFlags", DWORD),
    )


if TYPE_CHECKING:
    PCERT_CHAIN_PARA = pointer[CERT_CHAIN_PARA]  # type: ignore[misc]
else:
    PCERT_CHAIN_PARA = POINTER(CERT_CHAIN_PARA)


class CERT_TRUST_STATUS(Structure):
    _fields_ = (
        ("dwErrorStatus", DWORD),
        ("dwInfoStatus", DWORD),
    )


class CERT_CHAIN_ELEMENT(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("pCertContext", PCERT_CONTEXT),
        ("TrustStatus", CERT_TRUST_STATUS),
        ("pRevocationInfo", c_void_p),
        ("pIssuanceUsage", PCERT_ENHKEY_USAGE),
        ("pApplicationUsage", PCERT_ENHKEY_USAGE),
        ("pwszExtendedErrorInfo", LPCWSTR),
    )


PCERT_CHAIN_ELEMENT = POINTER(CERT_CHAIN_ELEMENT)


class CERT_SIMPLE_CHAIN(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("TrustStatus", CERT_TRUST_STATUS),
        ("cElement", DWORD),
        ("rgpElement", POINTER(PCERT_CHAIN_ELEMENT)),
        ("pTrustListInfo", c_void_p),
        ("fHasRevocationFreshnessTime", BOOL),
        ("dwRevocationFreshnessTime", DWORD),
    )


PCERT_SIMPLE_CHAIN = POINTER(CERT_SIMPLE_CHAIN)


class CERT_CHAIN_CONTEXT(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("TrustStatus", CERT_TRUST_STATUS),
        ("cChain", DWORD),
        ("rgpChain", POINTER(PCERT_SIMPLE_CHAIN)),
        ("cLowerQualityChainContext", DWORD),
        ("rgpLowerQualityChainContext", c_void_p),
        ("fHasRevocationFreshnessTime", BOOL),
        ("dwRevocationFreshnessTime", DWORD),
    )


PCERT_CHAIN_CONTEXT = POINTER(CERT_CHAIN_CONTEXT)
PCCERT_CHAIN_CONTEXT = POINTER(PCERT_CHAIN_CONTEXT)


class SSL_EXTRA_CERT_CHAIN_POLICY_PARA(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("dwAuthType", DWORD),
        ("fdwChecks", DWORD),
        ("pwszServerName", LPCWSTR),
    )


class CERT_CHAIN_POLICY_PARA(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("dwFlags", DWORD),
        ("pvExtraPolicyPara", c_void_p),
    )


PCERT_CHAIN_POLICY_PARA = POINTER(CERT_CHAIN_POLICY_PARA)


class CERT_CHAIN_POLICY_STATUS(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("dwError", DWORD),
        ("lChainIndex", LONG),
        ("lElementIndex", LONG),
        ("pvExtraPolicyStatus", c_void_p),
    )


PCERT_CHAIN_POLICY_STATUS = POINTER(CERT_CHAIN_POLICY_STATUS)


class CERT_CHAIN_ENGINE_CONFIG(Structure):
    _fields_ = (
        ("cbSize", DWORD),
        ("hRestrictedRoot", HCERTSTORE),
        ("hRestrictedTrust", HCERTSTORE),
        ("hRestrictedOther", HCERTSTORE),
        ("cAdditionalStore", DWORD),
        ("rghAdditionalStore", c_void_p),
        ("dwFlags", DWORD),
        ("dwUrlRetrievalTimeout", DWORD),
        ("MaximumCachedCertificates", DWORD),
        ("CycleDetectionModulus", DWORD),
        ("hExclusiveRoot", HCERTSTORE),
        ("hExclusiveTrustedPeople", HCERTSTORE),
        ("dwExclusiveFlags", DWORD),
    )


PCERT_CHAIN_ENGINE_CONFIG = POINTER(CERT_CHAIN_ENGINE_CONFIG)
PHCERTCHAINENGINE = POINTER(HCERTCHAINENGINE)

X509_ASN_ENCODING = 0x00000001
PKCS_7_ASN_ENCODING = 0x00010000
CERT_STORE_PROV_MEMORY = b"Memory"
CERT_STORE_ADD_USE_EXISTING = 2
USAGE_MATCH_TYPE_OR = 1
OID_PKIX_KP_SERVER_AUTH = c_char_p(b"1.3.6.1.5.5.7.3.1")
CERT_CHAIN_REVOCATION_CHECK_END_CERT = 0x10000000
CERT_CHAIN_REVOCATION_CHECK_CHAIN = 0x20000000
CERT_CHAIN_POLICY_IGNORE_ALL_NOT_TIME_VALID_FLAGS = 0x00000007
CERT_CHAIN_POLICY_IGNORE_INVALID_BASIC_CONSTRAINTS_FLAG = 0x00000008
CERT_CHAIN_POLICY_ALLOW_UNKNOWN_CA_FLAG = 0x00000010
CERT_CHAIN_POLICY_IGNORE_INVALID_NAME_FLAG = 0x00000040
CERT_CHAIN_POLICY_IGNORE_WRONG_USAGE_FLAG = 0x00000020
CERT_CHAIN_POLICY_IGNORE_INVALID_POLICY_FLAG = 0x00000080
CERT_CHAIN_POLICY_IGNORE_ALL_REV_UNKNOWN_FLAGS = 0x00000F00
CERT_CHAIN_POLICY_ALLOW_TESTROOT_FLAG = 0x00008000
CERT_CHAIN_POLICY_TRUST_TESTROOT_FLAG = 0x00004000
AUTHTYPE_SERVER = 2
CERT_CHAIN_POLICY_SSL = 4
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

# Flags to set for SSLContext.verify_mode=CERT_NONE
CERT_CHAIN_POLICY_VERIFY_MODE_NONE_FLAGS = (
    CERT_CHAIN_POLICY_IGNORE_ALL_NOT_TIME_VALID_FLAGS
    | CERT_CHAIN_POLICY_IGNORE_INVALID_BASIC_CONSTRAINTS_FLAG
    | CERT_CHAIN_POLICY_ALLOW_UNKNOWN_CA_FLAG
    | CERT_CHAIN_POLICY_IGNORE_INVALID_NAME_FLAG
    | CERT_CHAIN_POLICY_IGNORE_WRONG_USAGE_FLAG
    | CERT_CHAIN_POLICY_IGNORE_INVALID_POLICY_FLAG
    | CERT_CHAIN_POLICY_IGNORE_ALL_REV_UNKNOWN_FLAGS
    | CERT_CHAIN_POLICY_ALLOW_TESTROOT_FLAG
    | CERT_CHAIN_POLICY_TRUST_TESTROOT_FLAG
)

wincrypt = WinDLL("crypt32.dll")
kernel32 = WinDLL("kernel32.dll")


def _handle_win_error(result: bool, _: Any, args: Any) -> Any:
    if not result:
        # Note, actually raises OSError after calling GetLastError and FormatMessage
        raise WinError()
    return args


CertCreateCertificateChainEngine = wincrypt.CertCreateCertificateChainEngine
CertCreateCertificateChainEngine.argtypes = (
    PCERT_CHAIN_ENGINE_CONFIG,
    PHCERTCHAINENGINE,
)
