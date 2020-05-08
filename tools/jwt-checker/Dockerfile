FROM golang:1.14.2-buster AS build

RUN apt update && apt upgrade -y

COPY jwtvalidator/ /jwtvalidator

WORKDIR /jwtvalidator

RUN go build -o jwtchk

FROM alpine:3.11.6

WORKDIR /root/

COPY --from=build /jwtvalidator/jwtchk .

ENTRYPOINT ["./jwtchk"]
