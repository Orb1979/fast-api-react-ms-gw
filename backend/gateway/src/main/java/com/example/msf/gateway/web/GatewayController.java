package com.example.msf.gateway.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.core.annotation.AuthenticationPrincipal;

@RestController
public class GatewayController {

    @GetMapping("/gateway")
    public String gatewayTest(@AuthenticationPrincipal Jwt jwt) {
        // Test gateway, jwt contains claims, e.g. sub, email, roles,
        // without a valid JWT token this code will never be reached.
        return "Hit secure gateway, " + jwt.getClaimAsString("sub");
    }

    @GetMapping("/public/gateway")
    public String gatewayTest() {
        // Test public  gateway, no JWT token needed
        return "Hit public gateway (no JWT required)";
    }
}
