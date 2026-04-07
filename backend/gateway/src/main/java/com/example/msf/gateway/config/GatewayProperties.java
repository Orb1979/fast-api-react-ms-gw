package com.example.msf.gateway.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import java.util.Map;

@Configuration
@ConfigurationProperties(prefix = "gateway")
@Data
public class GatewayProperties {
    // Map of microservice keys to their base URLs.
    // e.g. customer -> http://localhost:8081/api/customer
    private Map<String, String> services;
}