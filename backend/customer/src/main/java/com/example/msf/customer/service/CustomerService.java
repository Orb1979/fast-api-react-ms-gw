package com.example.msf.customer.service;

import com.example.msf.customer.model.Customer;
import com.example.msf.customer.repository.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class CustomerService {
    private final CustomerRepository repository;

    public List<Customer> findAll() {
        return repository.findAll();
    }

    public Optional<Customer> findOne(Long id) {
        return repository.findById(id);
    }

    public Customer create(Customer customer) {
        return repository.save(customer);
    }

    public Optional<Customer> update(Long id, Customer customer) {
        return repository.findById(id)
                .map(existing -> {
                    existing.setName(customer.getName());
                    existing.setEmail(customer.getEmail());
                    existing.setPhoneNumber(customer.getPhoneNumber());
                    return repository.save(existing);
                });
    }

    public boolean delete(Long id) {
        if (!repository.existsById(id)) {
            return false;
        }
        repository.deleteById(id);
        return true;
    }
}
