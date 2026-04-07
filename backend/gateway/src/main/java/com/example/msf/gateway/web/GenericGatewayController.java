package com.example.msf.gateway.web;

import com.example.msf.gateway.config.GatewayProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.log4j.Log4j2;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.reactive.function.client.WebClient;

import jakarta.servlet.http.HttpServletRequest;
import java.util.Map;

@Log4j2
@RestController
@RequiredArgsConstructor
@RequestMapping("/api")
public class GenericGatewayController {

    private final WebClient.Builder webClientBuilder;
    private final GatewayProperties gatewayProperties;

    @RequestMapping("/**")
    public Object forward(
            @RequestBody(required = false) Object body,
            @RequestHeader Map<String, String> headers,
            @RequestParam Map<String, String> queryParams,
            HttpServletRequest request) {

        // Determine HTTP method
        String method = request.getMethod(); // GET, POST, PUT, DELETE, etc.

        // Extract path after /api/
        String fullPath = request.getRequestURI().substring(request.getContextPath().length() + "/api/".length());
        String[] segments = fullPath.split("/", 2);
        String serviceKey = segments[0];
        String downstreamPath = segments.length > 1 ? "/" + segments[1] : "";

        String baseUrl = gatewayProperties.getServices().get(serviceKey);
        if (baseUrl == null) {
            throw new RuntimeException("Unknown service: " + serviceKey);
        }

        log.info("{} {} forwarding to {}{}", method, fullPath, serviceKey, downstreamPath);

        // Build WebClient
        WebClient client = webClientBuilder.baseUrl(baseUrl).build();

        // Prepare request spec (method, uri, query params)
        WebClient.RequestBodySpec reqSpec = client
                .method(org.springframework.http.HttpMethod.valueOf(method))
                .uri(uriBuilder -> {
                    uriBuilder.path(downstreamPath);
                    queryParams.forEach(uriBuilder::queryParam);
                    return uriBuilder.build();
                });

        // Copy headers (except Host)
        // Host header would be the SPA domain and we don't want to forward to the host, but to the microservice
        // The WebClient automatically sets the Host header to match the actual downstream URL
        headers.forEach((k, v) -> {
            if (!k.equalsIgnoreCase(HttpHeaders.HOST)) {
                reqSpec.header(k, v);
            }
        });

        // Attach JWT from SecurityContext
        Jwt jwt = (Jwt) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
        reqSpec.header(HttpHeaders.AUTHORIZATION, "Bearer " + jwt.getTokenValue());

        // Attach body if present
        if (body != null) {
            reqSpec.contentType(MediaType.APPLICATION_JSON).bodyValue(body);
        }

        // Execute request (blocking)
        if (method.equalsIgnoreCase("DELETE")) {
            reqSpec.retrieve().toBodilessEntity().block();
            return null; // DELETE usually has no body
        } else {
            return reqSpec.retrieve().bodyToMono(Object.class).block();
        }
    }
}

/*
- Fully generic for all microservices:
  - /api/customer/** → customer service
  - /api/order/** → order service
  - /api/product/** → product service
- Supports all HTTP methods:
  - GET, POST, PUT, DELETE, PATCH
  - Automatically reads method from HttpServletRequest
- Handles headers, query params, and JSON body
- JWT propagated automatically from SecurityContext
- Blocking but safe in Spring MVC:
  - Uses .block() on bodyToMono(Object.class)
  - Works perfectly with spring-boot-starter-web
- No reactive WebFlux controller required:
  - You just need the spring-boot-starter-webflux dependency for WebClient.
*/

