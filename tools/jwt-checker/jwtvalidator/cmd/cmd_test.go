/*
 * Copyright 2020 Banco Bilbao Vizcaya Argentaria, S.A.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package cmd_test

import (
	"strings"
	"testing"

	"github.com/BBVA/apicheck/tools/jwt-checker/jwtvalidator/cmd"
	"github.com/BBVA/apicheck/tools/jwt-checker/jwtvalidator/validations"
)

func TestReturnOKWhenNoOptionsOrArgumentsGiven(t *testing.T) {
	o := cmd.ProgramOptions{}

	if e := cmd.Run(o); 2 != e.Code || "" == e.Error() {
		t.Errorf("Run raised an unexpected error. Expected: (2, %q); got: (%d, %q)", "", e.Code, e.Error())
	}
}

func TestReturnOKWhenHelpRequested(t *testing.T) {
	o := cmd.ProgramOptions{HelpRequested: true, FlagsProcessed: 1}

	if e := cmd.Run(o); 2 != e.Code || "" == e.Error() {
		t.Errorf("Run raised an unexpected error. Expected: (2, %q); got: (%d, %q)", "", e.Code, e.Error())
	}
}

func TestReturnOKWhenVersionRequested(t *testing.T) {
	o := cmd.ProgramOptions{VersionRequested: true, FlagsProcessed: 1}

	if e := cmd.Run(o); 0 != e.Code || "\nVersion 1.0.0" != e.Error() {
		t.Errorf("Run raised an unexpected error. Expected: (0, %q); got: (%d, %q)", "\nVersion 1.0.0", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedAndNoSecretGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false}, FlagsProcessed: 1}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nSecret for validating signature must be provided" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nSecret for validating signature must be provided", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedSecretAndInvalidNotBeforeGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret", IssuedBefore: "20200301T12:30"}, FlagsProcessed: 2}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nInvalid date format for issuedBefore. Should be YYYYMMDDThh:mm:ss" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nInvalid date format for issuedBefore. Should be YYYYMMDDThh:mm:ss", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedSecretAndInvalidExpiresAtGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret", ExpiresAt: "20200301T12:30"}, FlagsProcessed: 2}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nInvalid date format for expiresAt. Should be YYYYMMDDThh:mm:ss" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nInvalid date format for expiresAt. Should be YYYYMMDDThh:mm:ss", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedAndSecretGivenButTokenNotGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nOne and only one token must be provided" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nOne and only one token must be provided", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedAndSecretGivenButMoreThanATokenGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"FOO_BAR_TOKEN", "FOO_BAR_TOKEN"}}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nOne and only one token must be provided" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nOne and only one token must be provided", e.Code, e.Error())
	}
}

func TestKOWhenNotAllowUnsignedAndSecretGivenButInvalidTokenGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"FOO_BAR_TOKEN"}}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \njwt: token format is not valid" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \njwt: token format is not valid", e.Code, e.Error())
	}
}

func TestKOWhenInputExpectedAndNotGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"-"}, StdIn: strings.NewReader("")}

	if e := cmd.Run(o); 1 != e.Code || !strings.HasPrefix(e.Error(), "Errors: \nError reading standard Input") {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nError reading standard Input...", e.Code, e.Error())
	}
}

func TestKOWhenInvalidJSONInputGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"-"}, StdIn: strings.NewReader(`{"":"}`)}

	if e := cmd.Run(o); 1 != e.Code || !strings.HasPrefix(e.Error(), "Errors: \nJSON Error: ") {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nJSON Error: ...", e.Code, e.Error())
	}
}

func TestKOWhenNoAuthorizationHeaderExists(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"-"}, StdIn: strings.NewReader(`{"request":{"headers":{"Accept":"*/*"}}}`)}

	if e := cmd.Run(o); 1 != e.Code || !strings.HasPrefix(e.Error(), "Errors: \nNo Authorization header was found") {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nNo Authorization header was found", e.Code, e.Error())
	}
}

func TestKOWhenAuthorizationHeaderDontHaveBearer(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"-"}, StdIn: strings.NewReader(`{"request":{"headers":{"Authorization":"foo-auth"}}}`)}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \nNo Authorization bearer was found" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \nNo Authorization bearer was found", e.Code, e.Error())
	}
}

func TestKOWhenInvalidBearerTokenGiven(t *testing.T) {
	o := cmd.ProgramOptions{Options: validations.Options{AllowUnsignedTokens: false, Secret: "FOO_secret"}, FlagsProcessed: 2, Arguments: []string{"-"}, StdIn: strings.NewReader(`{"request":{"headers":{"Authorization":"Bearer FOO_BAR_TOKEN"}}}`)}

	if e := cmd.Run(o); 1 != e.Code || "Errors: \njwt: token format is not valid" != e.Error() {
		t.Errorf("Run didn't raise the expected error. Expected: (1, %q); got: (%d, %q)", "Errors: \njwt: token format is not valid", e.Code, e.Error())
	}
}
