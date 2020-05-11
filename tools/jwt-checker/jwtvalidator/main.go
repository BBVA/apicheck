package main

import (
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	jwt2 "github.com/cristalhq/jwt/v2"
)

const (
	VERSION = "1.0.0"
)

type listFlag []string

func (l *listFlag) String() string { return strings.Join(*l, ", ") }

func (l *listFlag) Set(value string) error {
	*l = append(*l, value)
	return nil
}

type options struct {
	helpRequested       bool
	versionRequested    bool
	allowUnsignedTokens bool
	allowedSignAlgs     listFlag
	secret              string
	issuer              string
	subject             string
	permittedFor        string
	issuedBefore        string
	timeIssuedBefore    time.Time
	expiresAt           string
	timeExpiresAt       time.Time
}

var programOptions options

var base64Decode = base64.RawURLEncoding.Decode

func main() {
	initOptions()

	flag.Parse()

	if programOptions.helpRequested || (flag.NArg() == 0 && flag.NFlag() == 0) {
		flag.Usage()
		os.Exit(0)
	}

	if programOptions.versionRequested {
		fmt.Fprintf(os.Stderr, "%s version %s\n", os.Args[0], VERSION)
		os.Exit(0)
	}

	if !programOptions.allowUnsignedTokens && programOptions.secret == "" {
		fmt.Fprint(os.Stderr, "Secret for validating signature must be provided\n")
		os.Exit(1)
	}

	if programOptions.issuedBefore != "" {
		var err error
		if programOptions.timeIssuedBefore, err = time.Parse(time.RFC3339, programOptions.issuedBefore); err != nil {
			fmt.Fprintf(os.Stderr, "Invalid date format for %s. Shoild be YYYYMMDDThh:mm:ss\n", "issuedBefore")
			os.Exit(1)
		}
	}

	if programOptions.expiresAt != "" {
		var err error
		if programOptions.timeExpiresAt, err = time.Parse(time.RFC3339, programOptions.expiresAt); err != nil {
			fmt.Fprintf(os.Stderr, "Invalid date format for %s. Shoild be YYYYMMDDThh:mm:ss\n", "expiresAt")
			os.Exit(1)
		}
	}

	switch flag.NArg() {
	case 1:
		if err := validateToken(([]byte)(flag.Arg(0)), programOptions); err != nil {
			for _, e := range err {
				fmt.Println(e)
			}
			os.Exit(1)
		}
		os.Exit(0)
	default: /*Only one token must be provided or - to read from standard input*/
		fmt.Fprint(os.Stderr, "One and only one token must be provided\n")
		os.Exit(1)
	}
}

func validateToken(rawToken []byte, opt options) []error {
	valError := []error{}

	token, errParse := jwt2.Parse(rawToken)
	if errParse != nil {
		panic(errParse)
	}

	// fmt.Printf("Algorithm %v\n", token.Header().Algorithm)
	// fmt.Printf("Type      %v\n", token.Header().Type)
	// fmt.Printf("Claims    %v\n", string(token.RawClaims()))
	// fmt.Printf("Payload   %v\n", string(token.Payload()))
	// fmt.Printf("Token     %v\n", string(token.Raw()))

	// Validate signature
	if v, err := getSignValidator(token.Header().Algorithm, opt.secret); err != nil {
		panic(err)
	} else {
		token, errSign := jwt2.ParseAndVerify(rawToken, v)
		if errSign != nil {
			valError = append(valError, errSign)
		} else {
			// Validate header
			if err := validateJWTHeader(token.Header(), opt); err != nil {
				valError = append(valError, err...)
			}

			// Validate claims
			claims := &jwt2.StandardClaims{}
			_ = json.Unmarshal(token.RawClaims(), claims)
			if err := validateJWTStdClaims(*claims, opt); err != nil {
				valError = append(valError, err...)
			}
		}
	}

	if len(valError) > 0 {
		return valError
	} else {
		return nil
	}
	// Output:
	// Algorithm HS256
	// Type      JWT
	// Claims    {"aud":"admin","jti":"random-unique-string"}
	// Payload   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImp0aSI6InJhbmRvbS11bmlxdWUtc3RyaW5nIn0
	// Token     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImp0aSI6InJhbmRvbS11bmlxdWUtc3RyaW5nIn0.dv9-XpY9P8ypm1uWQwB6eKvq3jeyodLA7brhjsf4JVs
}

func getSignValidator(alg jwt2.Algorithm, secret string) (jwt2.Verifier, error) {

	//buf := []byte(secret)
	// Base64 decode secret
	buf := make([]byte, len(secret))
	if n, err := base64Decode(buf, []byte(secret)); err != nil {
		return nil, err
	} else {
		buf = buf[:n-1]
	}

	switch alg {
	//	case jwt2.EdDSA:
	//		// Create public key from byte array
	//		var pubKey ed25519.PrivateKey
	//		if , err := jwt2.NewVerifierEdDSA(pubKey); err != nil {
	//			return v, nil
	//		} else {
	//			return nil, err
	//		}
	//	case jwt2.ES256, jwt2.ES384, jwt2.ES512:
	//		// Create public key from byte array
	//		var pubKey *ecdsa.PublicKey
	//    if s, err := jwt2.NewVerifierES(alg, ); err != nil {
	//			return s, nil
	//		} else {
	//			return nil, err
	//		}
	case jwt2.HS256, jwt2.HS384, jwt2.HS512:
		if v, err := jwt2.NewVerifierHS(alg, buf); err == nil {
			return v, nil
		} else {
			return nil, err
		}
	//	case jwt2.PS256, jwt2.PS384, jwt2.PS512:
	//		// Create public key from byte array
	//		var pubKey *rsa.PublicKey
	//    if v, err := jwt2.NewVerifierPS(alg, pubKey); err != nil {
	//			return v, nil
	//		} else {
	//			return nil, err
	//		}
	//	case jwt2.RS256, jwt2.RS384, jwt2.RS512:
	//		// Create public key from byte array
	//		var pubKey *rsa.PublicKey
	//		if v, err := jwt2.NewVerifierRS(alg, pubKey); err != nil {
	//			return s, nil
	//		} else {
	//			return nil, err
	//		}
	default:
		return nil, fmt.Errorf("Unsupported Algorithm: %s", alg)
	}

}

func initOptions() {
	flag.BoolVar(&programOptions.helpRequested, "h", false, "show help message and exit")
	flag.BoolVar(&programOptions.versionRequested, "V", false, "show version info and exit")

	flag.BoolVar(&programOptions.allowUnsignedTokens, "unsig", false, "don't raise an error if token is unsigned (algorithm \"none\")")
	flag.Var(&programOptions.allowedSignAlgs, "allowAlg", "raise an error if token has different signing algorithm. Provide several options if you want to allow more than one algorithm")
	flag.StringVar(&programOptions.secret, "secret", "", "use this secret to validate the sign. Base64 encoded (mandatory when validating signed tokens)")
	flag.StringVar(&programOptions.issuer, "issuer", "", "raise an error if token has different issuer")
	flag.StringVar(&programOptions.subject, "subject", "", "raise an error if token has different subject")
	flag.StringVar(&programOptions.permittedFor, "audience", "", "raise an error if token has different audience")
	flag.StringVar(&programOptions.issuedBefore, "notBefore", "", "raise an error if the not before date is priot to this. Format: YYYY-MM-DDThh:mm:ss")
	flag.StringVar(&programOptions.expiresAt, "expiresAt", "", "raise an error if the expiration date is after this. Format: YYYY-MM-DDThh:mm:ss")

}

func validateJWTHeader(header jwt2.Header, opt options) []error {
	errors := []error{}

	if header.Type != "JWT" || (header.ContentType != "" && header.ContentType != "JWT") {
		errors = append(errors, fmt.Errorf("JWT type (%s, %s) not supported", header.Type, header.ContentType))
	}
	if !opt.allowUnsignedTokens && header.Algorithm == "none" {
		errors = append(errors, fmt.Errorf("JWT is unsigned"))
	}
	if len(opt.allowedSignAlgs) > 0 {
		found := false
		for _, alg := range opt.allowedSignAlgs {
			if header.Algorithm == jwt2.Algorithm(alg) {
				found = true
				break
			}
		}
		if !found {
			errors = append(errors, fmt.Errorf("JWT signing algorithm (%s) is not allowed", header.Algorithm))
		}
	}

	return errors
}

func validateJWTStdClaims(claims jwt2.StandardClaims, opt options) []error {
	errors := make([]error, 0)

	if claims.Issuer == "" {
		errors = append(errors, fmt.Errorf("No issuer claim found"))
	} else if opt.issuer != "" && !claims.IsIssuer(opt.issuer) {
		errors = append(errors, fmt.Errorf("Issuer claim doesn't match. Expected: %s, got: %s", opt.issuer, claims.Issuer))
	}
	if claims.Subject == "" {
		errors = append(errors, fmt.Errorf("No subject claim found"))
	} else if opt.subject != "" && !claims.IsSubject(opt.subject) {
		errors = append(errors, fmt.Errorf("Subject claim doesn't match. Expected: %s, got: %s", opt.subject, claims.Subject))
	}
	if len(claims.Audience) == 0 {
		errors = append(errors, fmt.Errorf("No audience claim found"))
	} else if opt.permittedFor != "" && !claims.IsForAudience(opt.permittedFor) {
		errors = append(errors, fmt.Errorf("Audience claim doesn't match. Expected: %s, got: %s", opt.permittedFor, strings.Join(claims.Audience, ",")))
	}
	if opt.issuedBefore != "" && !claims.IsValidNotBefore(opt.timeIssuedBefore) {
		errors = append(errors, fmt.Errorf("NotBefore claim doesn't match. Expected: %s, got: %v", opt.issuedBefore, claims.NotBefore))
	}
	if opt.expiresAt != "" && !claims.IsValidExpiresAt(opt.timeExpiresAt) {
		errors = append(errors, fmt.Errorf("ExpiresAt claim doesn't match. Expected: %s, got: %v", opt.expiresAt, claims.ExpiresAt))
	}

	//  jwt2.AudienceChecker([]string{"admin"}),
	//  jwt2.IDChecker("random-unique-string"),

	return errors
}

// mySecretPassword = bXlTZWNyZXRQYXNzd29yZAo=
// mySecretPasswordmySecretPassword = bXlTZWNyZXRQYXNzd29yZG15U2VjcmV0UGFzc3dvcmQK
/*******************************************************************************
/* header.typ === "JWT"
/* header.alg !=="none" except Options.allowUnsignedTokens
/* header.alg in Options.allowedSignAlgs
token is signed
/* payload.issuer !=== ""
/* payload.issuer ==== Options.issuer
/* payload.subject !=== ""
/* payload.subject ==== Options.subject
/* payload.audience !=== ""
/* payload.audience ==== Options.permittedFor
¿¿payload.IsValidNow === ok??
payload.NotBeforeChecker(Options.issuedBefore) === ok
payload.ExpirationTimeChecker(Options.expiresAt) === ok
*******************************************************************************/
