package main

import (
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"strings"
	"time"

	"github.com/BBVA/apicheck/tools/jwt-checker/jwtvalidator/headerval"

	"github.com/cristalhq/jwt"
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

func ValidateToken(rawToken []byte, headVal *headerval.Validator, claimVal *jwt.Validator, secret string) []error {
	valError := []error{}

	token, errParse := jwt.Parse(rawToken)
	if errParse != nil {
		panic(errParse)
	}

	// fmt.Printf("Algorithm %v\n", token.Header().Algorithm)
	// fmt.Printf("Type      %v\n", token.Header().Type)
	// fmt.Printf("Claims    %v\n", string(token.RawClaims()))
	// fmt.Printf("Payload   %v\n", string(token.Payload()))
	// fmt.Printf("Token     %v\n", string(token.Raw()))

	// Validate signature
	// token, errSign := jwt.ParseAndVerify(rawToken, getSignValidator(token.Header().Algorithm, secret))
	// if errSign != nil {
	// 	panic(errSign)
	// }

	// Validate header
	header := &jwt.Header{}
	_ = json.Unmarshal(token.RawHeader(), header)
	errValHeader := headVal.ValidateAll(header)
	if errValHeader != nil {
		valError = append(valError, errValHeader...)
	}

	// Validate claims
	claims := &jwt.StandardClaims{}
	_ = json.Unmarshal(token.RawClaims(), claims)

	errValClaims := claimVal.ValidateAll(claims)
	if errValClaims != nil {
		valError = append(valError, errValClaims...)
	}

	return valError
	// Output:
	// Algorithm HS256
	// Type      JWT
	// Claims    {"aud":"admin","jti":"random-unique-string"}
	// Payload   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImp0aSI6InJhbmRvbS11bmlxdWUtc3RyaW5nIn0
	// Token     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhZG1pbiIsImp0aSI6InJhbmRvbS11bmlxdWUtc3RyaW5nIn0.dv9-XpY9P8ypm1uWQwB6eKvq3jeyodLA7brhjsf4JVs
}

func getSignValidator(alg jwt.Algorithm, secret string) (jwt.Signer, error) {

	switch alg {
	//	case jwt.EdDSA:
	//		var publicKey ed25519.PublicKey
	//		if s, err := jwt.NewEdDSA(publicKey, nil); err != nil {
	//			return s, nil
	//		} else {
	//			return nil, err
	//		}
	//	case jwt.ES256, jwt.ES384, jwt.ES512:
	//    if s, err := jwt.; err != nil {
	//			return s, nil
	//		} else {
	//			return nil, err
	//		}
	case jwt.HS256:
		buf := make([]byte, len(secret))
		var (
			n   = 0
			err error
		)
		if n, err = base64Decode(buf, []byte(secret)); err != nil {
			return nil, err
		}
		if s, err := jwt.NewHS256(buf[:n]); err != nil {
			return s, nil
		} else {
			return nil, err
		}
	case jwt.HS384:
		buf := make([]byte, len(secret))
		var (
			n   = 0
			err error
		)
		if n, err = base64Decode(buf, []byte(secret)); err != nil {
			return nil, err
		}
		if s, err := jwt.NewHS384(buf[:n]); err != nil {
			return s, nil
		} else {
			return nil, err
		}
	case jwt.HS512:
		buf := make([]byte, len(secret))
		var (
			n   = 0
			err error
		)
		if n, err = base64Decode(buf, []byte(secret)); err != nil {
			return nil, err
		}
		if s, err := jwt.NewHS512(buf[:n]); err != nil {
			return s, nil
		} else {
			return nil, err
		}
		//	case jwt.PS256, jwt.PS384, jwt.PS512:
		//    if s, err := jwt.; err != nil {
		//			return s, nil
		//		} else {
		//			return nil, err
		//		}
		//	case jwt.RS256, jwt.RS384, jwt.RS512:
		//    if s, err := jwt.; err != nil {
		//			return s, nil
		//		} else {
		//			return nil, err
		//		}
	default:
		return nil, fmt.Errorf("Unsupported Algorithm: %s", alg)
	}

}

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
		ValidateToken(([]byte)(flag.Arg(0)), generateHeaderValidator(programOptions), generateClaimsValidator(programOptions), programOptions.secret)
	default: /*Only one token must be provided or - to read from standard input*/
		fmt.Fprint(os.Stderr, "Only one token must be provided\n")
		os.Exit(1)
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

func generateClaimsValidator(opt options) *jwt.Validator {
	checks := make([]jwt.Check, 0)

	checks = append(checks, func(claims *jwt.StandardClaims) error {
		if claims.Issuer == "" {
			return fmt.Errorf("No issuer claim found")
		}
		return nil
	})
	if opt.issuer != "" {
		checks = append(checks, jwt.IssuerChecker(opt.issuer))
	}
	checks = append(checks, func(claims *jwt.StandardClaims) error {
		if claims.Subject == "" {
			return fmt.Errorf("No subject claim found")
		}
		return nil
	})
	if opt.subject != "" {
		checks = append(checks, jwt.SubjectChecker(opt.subject))
	}
	checks = append(checks, func(claims *jwt.StandardClaims) error {
		if len(claims.Audience) == 0 {
			return fmt.Errorf("No audience claim found")
		}
		return nil
	})
	if opt.permittedFor != "" {
		checks = append(checks, jwt.AudienceChecker([]string{opt.permittedFor}))
	}
	if opt.issuedBefore != "" {
		checks = append(checks, jwt.NotBeforeChecker(opt.timeIssuedBefore))
	}
	if opt.expiresAt != "" {
		checks = append(checks, jwt.ExpirationTimeChecker(opt.timeExpiresAt))
	}

	validator := jwt.NewValidator(checks...)
	//  jwt.AudienceChecker([]string{"admin"}),
	//  jwt.IDChecker("random-unique-string"),

	return validator
}

func generateHeaderValidator(opt options) *headerval.Validator {
	checks := []headerval.Check{headerval.TokenTypeChecker()}

	if !opt.allowUnsignedTokens {
		checks = append(checks, headerval.SignedTokenChecker())
	}
	if len(opt.allowedSignAlgs) > 0 {
		checks = append(checks, headerval.AllowedSignAlgorithmChecker(opt.allowedSignAlgs))
	}

	return headerval.NewValidator(checks...)
}

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
