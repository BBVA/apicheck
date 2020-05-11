package headerval

import (
	"fmt"

	"github.com/cristalhq/jwt/v2"
)

type Check func(header *jwt.Header) error

type Validator struct {
	checks []Check
}

func NewValidator(checks ...Check) *Validator {
	return &Validator{checks}
}

func (v *Validator) Validate(header *jwt.Header) error {
	for _, check := range v.checks {
		if err := check(header); err != nil {
			return err
		}
	}

	return nil
}

func (v *Validator) ValidateAll(header *jwt.Header) []error {
	errors := make([]error, 0)
	for _, check := range v.checks {
		if err := check(header); err != nil {
			errors = append(errors, err)
		}
	}

	return errors
}

func TokenTypeChecker() Check {
	return func(header *jwt.Header) error {
		if header.Type != "JWT" || header.ContentType != "JWT" {
			return fmt.Errorf("JWT type (%s, %s) not supported", header.Type, header.ContentType)
		}
		return nil
	}
}

func SignedTokenChecker() Check {
	return func(header *jwt.Header) error {
		if header.Algorithm == "none" {
			return fmt.Errorf("JWT is unsigned")
		}
		return nil
	}
}

func AllowedSignAlgorithmChecker(algs []string) Check {
	return func(header *jwt.Header) error {
		for _, alg := range algs {
			if header.Algorithm == jwt.Algorithm(alg) {
				return nil
			}
		}
		return fmt.Errorf("JWT signing algorithm (%s) is not allowed", header.Algorithm)
	}
}

func KeyIDChecker(keyId string) Check {
	return func(header *jwt.Header) error {
		if header.KeyID != keyId {
			return fmt.Errorf("JWT keyID (%s) doesn't match", header.KeyID)
		}
		return nil
	}
}
