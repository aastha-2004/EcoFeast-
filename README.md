# EcoFeast-
CREATE DATABASE EcoFeast;

USE EcoFeast;

-- Users Table
CREATE TABLE USERS (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    user_type ENUM('donor', 'recipient', 'admin') NOT NULL
);

-- Food Donations Table
CREATE TABLE DONATIONS (
    donation_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    food_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    expiry_date DATE NOT NULL,
    pickup_location VARCHAR(255) NOT NULL,
    status ENUM('pending', 'picked_up', 'delivered') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES USERS(user_id) ON DELETE CASCADE
);

-- Food Requests Table
CREATE TABLE REQUESTS (
    request_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    donation_id INT,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'rejected', 'fulfilled') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES USERS(user_id),
    FOREIGN KEY (donation_id) REFERENCES DONATIONS(donation_id)
);

-- Bio-Waste Management Table
CREATE TABLE BIOWASTE (
    waste_id INT PRIMARY KEY AUTO_INCREMENT,
    donation_id INT,
    disposal_status ENUM('pending', 'processed', 'disposed') DEFAULT 'pending',
    disposal_facility VARCHAR(255),
    disposal_date TIMESTAMP NULL,
    FOREIGN KEY (donation_id) REFERENCES DONATIONS(donation_id)
);

import axios from 'axios';

const API_URL = "http://127.0.0.1:8000/api/";

export const loginUser = async (email, password) => {
    return await axios.post(${API_URL}login/, { email, password });
};

export const fetchDonations = async () => {
    return await axios.get(${API_URL}donations/);
};

export const requestFood = async (donationId, userId) => {
    return await axios.post(${API_URL}requests/, { donationId, userId });
};

import React, { useState } from 'react';
import { loginUser } from './api';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await loginUser(email, password);
        console.log(response.data);
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default Login;

import React, { useEffect, useState } from 'react';
import { fetchDonations } from './api';

function Home() {
    const [donations, setDonations] = useState([]);

    useEffect(() => {
        async function getData() {
            const response = await fetchDonations();
            setDonations(response.data);
        }
        getData();
    }, []);

    return (
        <div>
            <h2>Available Food Donations</h2>
            <ul>
                {donations.map((item) => (
                    <li key={item.donation_id}>
                        {item.food_name} - {item.quantity}kg (Expiry: {item.expiry_date})
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Home;



EcoFeast is a technology-driven platform designed to combat food waste and hunger in India by connecting surplus food donors, such as restaurants, hotels, and individuals, with NGOs and food banks. It leverages AI and ML for food categorization and demand prediction, while IoT sensors ensure food quality and safety. Route optimization minimizes transportation costs and improves efficiency, and real-time tracking enhances transparency. The user-friendly app makes food donation accessible to all demographics. EcoFeast also ensures compliance with food safety and legal regulations, preventing risks. By collaborating with NGOs, local governments, and businesses, it aims to create a scalable and sustainable food redistribution system that reduces waste and provides meals to the needy.
