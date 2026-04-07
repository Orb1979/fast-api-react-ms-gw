import { useEffect, useState } from "react";
import { useCustomerService } from "../services/customerService";

export default function CustomerManager() {
    const { getCustomers, createCustomer, deleteCustomer } = useCustomerService();
    const [customers, setCustomers] = useState([]);
    const [form, setForm] = useState({ name: "", email: "", phoneNumber: "" });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const loadCustomers = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getCustomers();
            setCustomers(data);
        } catch (e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        console.log("load  customers")
        loadCustomers();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        try {
            await createCustomer(form);
            setForm({ name: "", email: "", phoneNumber: "" });
            await loadCustomers();
        } catch (e) {
            setError(e.message);
        }
    };

    const handleDelete = async (id) => {
        setError(null);
        try {
            await deleteCustomer(id);
            await loadCustomers();
        } catch (e) {
            setError(e.message);
        }
    };

    return (
        <div>
            {error && <p style={{ color: "red" }}>Error: {error}</p>}

            <h2>Create Customer</h2>
            <form onSubmit={handleSubmit}>
                <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
                <input name="email" placeholder="Email" value={form.email} onChange={handleChange} />
                <input name="phoneNumber" placeholder="Phone number" value={form.phoneNumber} onChange={handleChange} />
                <button type="submit">Save</button>
            </form>

            <h2>Customers</h2>
            {loading ? (
                <p>Loading...</p>
            ) : customers.length === 0 ? (
                <p>No customers yet.</p>
            ) : (
                <table border="1" cellPadding="8">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {customers.map((c) => (
                        <tr key={c.id}>
                            <td>{c.id}</td>
                            <td>{c.name}</td>
                            <td>{c.email}</td>
                            <td>{c.phoneNumber}</td>
                            <td>
                                <button onClick={() => handleDelete(c.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}