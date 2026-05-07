FROM alpine:latest as builder

# Install git and openssh
RUN apk add --no-cache git openssh

# Clone the private repo
RUN mkdir -p ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh git clone git@github.com:Scoutboy06/vinyl-print.git /app

FROM nginx:alpine

# Copy static files from builder
COPY --from=builder /app/index.html /usr/share/nginx/html/
COPY --from=builder /app/styles.css /usr/share/nginx/html/
COPY --from=builder /app/script.js /usr/share/nginx/html/

EXPOSE 80
