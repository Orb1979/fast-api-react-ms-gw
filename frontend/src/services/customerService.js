import { useApi } from "./api";

const API_BASE = "/api/customer/customers";

export const useCustomerService = () => {
    const authFetch = useApi();

    const getCustomers = async () => {
        const res = await authFetch(API_BASE);
        if (!res.ok) throw new Error("Failed to load customers");
        return res.json();
    };

    const createCustomer = async (customer) => {
        const res = await authFetch(API_BASE, {
            method: "POST",
            body: JSON.stringify(customer),
        });
        if (!res.ok) throw new Error("Failed to create customer");
        return res.json();
    };

    const deleteCustomer = async (id) => {
        const res = await authFetch(`${API_BASE}/${id}`, { method: "DELETE" });
        if (!res.ok && res.status !== 204) throw new Error("Failed to delete customer");
    };

    return {
        getCustomers,
        createCustomer,
        deleteCustomer,
    };
};