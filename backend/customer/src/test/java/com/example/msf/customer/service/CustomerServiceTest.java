package com.example.msf.customer.service;

import com.example.msf.customer.model.Customer;
import com.example.msf.customer.repository.CustomerRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CustomerServiceTest {
    @InjectMocks
    CustomerService customerService;
    @Mock
    private CustomerRepository repository;
    private Customer existingCustomer;
    private Customer updatedData;

    @BeforeEach
    void setUp() {
        existingCustomer = new Customer();
        existingCustomer.setId(1L);
        existingCustomer.setName("Old Name");
        existingCustomer.setEmail("old@email.com");
        existingCustomer.setPhoneNumber("123");

        updatedData = new Customer();
        updatedData.setName("New Name");
        updatedData.setEmail("new@email.com");
        updatedData.setPhoneNumber("456");
    }

    @Test
    void update_shouldUpdateCustomer_whenExists() {
        // Arrange
        when(repository.findById(1L)).thenReturn(Optional.of(existingCustomer));
        when(repository.save(any(Customer.class))).thenAnswer(inv -> inv.getArgument(0));

        // Act
        Optional<Customer> result = customerService.update(1L, updatedData);

        // Assert
        assertTrue(result.isPresent());

        Customer updated = result.get();
        assertEquals("New Name", updated.getName());
        assertEquals("new@email.com", updated.getEmail());
        assertEquals("456", updated.getPhoneNumber());

        verify(repository).save(existingCustomer);
    }

    @Test
    void update_shouldReturnEmpty_whenNotFound() {
        // Arrange
        when(repository.findById(1L)).thenReturn(Optional.empty());

        // Act
        Optional<Customer> result = customerService.update(1L, updatedData);

        // Assert
        assertTrue(result.isEmpty());
        verify(repository, never()).save(any());
    }

    @Test
    void delete_shouldDelete_whenExists() {
        // Arrange
        when(repository.existsById(1L)).thenReturn(true);

        // Act
        boolean result = customerService.delete(1L);

        // Assert
        assertTrue(result);
        verify(repository).deleteById(1L);
    }

    @Test
    void delete_shouldReturnFalse_whenNotExists() {
        // Arrange
        when(repository.existsById(1L)).thenReturn(false);

        // Act
        boolean result = customerService.delete(1L);

        // Assert
        assertFalse(result);
        verify(repository, never()).deleteById(any());
    }
}