# LLM Output

=== FILE: src/App.jsx ===
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';
import { ToastContainer } from 'react-toastify';
import { AiOutlineLogin, AiOutlineUserAdd } from 'react-icons/ai';
import { FiLogOut } from 'react-icons/fi';
import { useForm } from 'react-hook-form';
import { clsx } from 'clsx';
import { format } from 'date-fns';

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [user, setUser] = useState(null);
  const [products, setProducts] = useState([]);
  const [totalProducts, setTotalProducts] = useState(0);
  const [lowStockAlerts, setLowStockAlerts] = useState(0);
  const [totalInventoryValue, setTotalInventoryValue] = useState(0);
  const [period, setPeriod] = useState('week');
  const [weekData, setWeekData] = useState([]);
  const [statusData, setStatusData] = useState([]);
  const [recentRecords, setRecentRecords] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [loginForm, setLoginForm] = useState(false);
  const [registerForm, setRegisterForm] = useState(false);

  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  const handleLogin = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/login`, data);
      setUser(response.data);
      setLoginForm(false);
    } catch (error) {
      console.error(error);
    }
  };

  const handleRegister = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/register`, data);
      setUser(response.data);
      setRegisterForm(false);
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    setUser(null);
  };

  const handleAddProduct = async (data) => {
    try {
      const response = await axios.post(`${BASE_URL}/products`, data);
      setProducts([...products, response.data]);
      setModalOpen(false);
    } catch (error) {
      console.error(error);
    }
  };

  const handlePeriodChange = (period) => {
    setPeriod(period);
  };

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/products`);
        const safeList = Array.isArray(response.data) ? response.data : (response.data?.items || []);
        setProducts(safeList);
        setTotalProducts(safeList.length);
        setLowStockAlerts(safeList.filter((product) => product.quantity < 5).length);
        setTotalInventoryValue(safeList.reduce((acc, product) => acc + product.price * product.quantity, 0));
      } catch (error) {
        console.error(error);
      }
    };

    fetchProducts();
  }, []);

  useEffect(() => {
    const fetchWeekData = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/week-data`);
        const safeList = Array.isArray(response.data) ? response.data : (response.data?.items || []);
        setWeekData(safeList);
      } catch (error) {
        console.error(error);
      }
    };

    fetchWeekData();
  }, []);

  useEffect(() => {
    const fetchStatusData = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/status-data`);
        const safeList = Array.isArray(response.data) ? response.data : (response.data?.items || []);
        setStatusData(safeList);
      } catch (error) {
        console.error(error);
      }
    };

    fetchStatusData();
  }, []);

  useEffect(() => {
    const fetchRecentRecords = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/recent-records`);
        const safeList = Array.isArray(response.data) ? response.data : (response.data?.items || []);
        setRecentRecords(safeList);
      } catch (error) {
        console.error(error);
      }
    };

    fetchRecentRecords();
  }, []);

  return (
    <HashRouter>
      <div className="h-screen flex flex-col">
        <header className="bg-gray-800 text-white p-4 flex justify-between">
          <h1 className="text-2xl font-bold">Inventory Management System</h1>
          {user ? (
            <div className="flex items-center">
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={handleLogout}>
                <FiLogOut size={20} />
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center">
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={() => setLoginForm(true)}>
                <AiOutlineLogin size={20} />
                Login
              </button>
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded ml-4" onClick={() => setRegisterForm(true)}>
                <AiOutlineUserAdd size={20} />
                Register
              </button>
            </div>
          )}
        </header>
        {user ? (
          <main className="flex-1 overflow-y-scroll p-4">
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Total Products</h2>
                <p className="text-2xl font-bold">{totalProducts}</p>
              </div>
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Low Stock Alerts</h2>
                <p className="text-2xl font-bold">{lowStockAlerts}</p>
              </div>
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Total Inventory Value</h2>
                <p className="text-2xl font-bold">${totalInventoryValue.toFixed(2)}</p>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-4 mb-4">
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Weekly Trend</h2>
                <div className="flex flex-wrap justify-between">
                  {weekData.map((data, index) => (
                    <div key={index} className="bg-gray-600 p-2 rounded mb-2" style={{ width: `${data.value}%` }}>
                      <p className="text-sm font-bold">{format(new Date(data.date), 'MMM dd')}</p>
                      <p className="text-sm font-bold">{data.value}%</p>
                    </div>
                  ))}
                </div>
              </div>
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Status Breakdown</h2>
                <div className="flex flex-wrap justify-between">
                  {statusData.map((data, index) => (
                    <div key={index} className="bg-gray-600 p-2 rounded mb-2" style={{ width: `${data.value}%` }}>
                      <p className="text-sm font-bold">{data.label}</p>
                      <p className="text-sm font-bold">{data.value}%</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 gap-4 mb-4">
              <div className="bg-gray-700 p-4 rounded">
                <h2 className="text-lg font-bold">Recent Records</h2>
                <table className="w-full">
                  <thead>
                    <tr>
                      <th className="text-sm font-bold">Date</th>
                      <th className="text-sm font-bold">Product</th>
                      <th className="text-sm font-bold">Quantity</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentRecords.map((record, index) => (
                      <tr key={index}>
                        <td className="text-sm">{format(new Date(record.date), 'MMM dd, yyyy')}</td>
                        <td className="text-sm">{record.product}</td>
                        <td className="text-sm">{record.quantity}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={() => setModalOpen(true)}>Add Product</button>
            <div className="flex justify-between mt-4">
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={() => handlePeriodChange('week')}>Week</button>
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={() => handlePeriodChange('month')}>Month</button>
              <button className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded" onClick={() => handlePeriodChange('year')}>Year</button>
            </div>
          </main>
        ) : (
          <main className="flex-1 flex justify-center items-center">
            {loginForm ? (
              <form onSubmit={handleSubmit(handleLogin)}>
                <h2 className="text-lg font-bold">Login</h2>
                <div className="mb-4">
                  <label className="block text-sm font-bold mb-2">Email</label>
                  <input type="email" {...register('email')} className="bg-gray-700 p-2 rounded" />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-bold mb-2">Password</label>
                  <input type="password" {...register('password')} className="bg-gray-700 p-2 rounded" />
                </div>
                <button type="submit" className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded">Login</button>
              </form>
            ) : registerForm ? (
              <form onSubmit={handleSubmit(handleRegister)}>
                <h2 className="text-lg font-bold">Register</h2>
                <div className="mb-4">
                  <label className="block text-sm font-bold mb-2">Email</label>
                  <input type="email" {...register('email')} className="bg-gray-700 p-2 rounded" />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-bold mb-2">Password</label>
                  <input type="password" {...register('password')} className="bg-gray-700 p-2 rounded" />
                </div>
                <div className="mb-4">
                  <label className="block text-sm font-bold mb-2">Confirm Password</label>
                  <input type="password" {...register('confirmPassword')} className="bg-gray-700 p-2 rounded" />
                </div>
                <button type="submit" className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded">Register</button>
              </form>
            ) : (
              <div>
                <h2 className="text-lg font-bold">Welcome to Inventory Management System</h2>
                <p className="text-sm">Please login or register to access the system.</p>
              </div>
            )}
          </main>
        )}
      </div>
      {modalOpen && (
        <div className="fixed top-0 left-0 w-full h-full bg-gray-800 bg-opacity-50 flex justify-center items-center">
          <div className="bg-gray-700 p-4 rounded">
            <h2 className="text-lg font-bold">Add Product</h2>
            <form onSubmit={handleSubmit(handleAddProduct)}>
              <div className="mb-4">
                <label className="block text-sm font-bold mb-2">Product Name</label>
                <input type="text" {...register('name')} className="bg-gray-600 p-2 rounded" />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-bold mb-2">Category</label>
                <input type="text" {...register('category')} className="bg-gray-600 p-2 rounded" />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-bold mb-2">SKU</label>
                <input type="text" {...register('sku')} className="bg-gray-600 p-2 rounded" />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-bold mb-2">Quantity</label>
                <input type="number" {...register('quantity')} className="bg-gray-600 p-2 rounded" />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-bold mb-2">Price</label>
                <input type="number" {...register('price')} className="bg-gray-600 p-2 rounded" />
              </div>
              <button type="submit" className="bg-gray-600 hover:bg-gray-700 px-4 py-2 rounded">Add Product</button>
            </form>
          </div>
        </div>
      )}
      <ToastContainer />
    </HashRouter>
  );
}

export default App;
=== END ===

=== FILE: src/main.jsx ===
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
=== END ===

=== FILE: src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  @apply bg-gray-900;
}

h1, h2, h3, h4, h5, h6 {
  @apply font-bold;
}

button {
  @apply transition-all duration-300 hover:scale-105;
}
=== END ===

=== FILE: src/api.js ===
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const login = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/login`, data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const register = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/register`, data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const getProducts = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/products`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const addProduct = async (data) => {
  try {
    const response = await axios.post(`${BASE_URL}/products`, data);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const getWeekData = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/week-data`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const getStatusData = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/status-data`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};

export const getRecentRecords = async () => {
  try {
    const response = await axios.get(`${BASE_URL}/recent-records`);
    return response.data;
  } catch (error) {
    console.error(error);
  }
};
=== END ===