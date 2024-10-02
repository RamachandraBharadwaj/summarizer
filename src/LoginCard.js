import React, { useState } from 'react';

const LoginCard = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = (e) => {
    e.preventDefault();
    // Hardcoded credentials for demo purposes
    if (username === 'user' && password === 'password123') {
      console.log('Login successful');
      onLoginSuccess();  // Notify App.js that the login was successful
    } else {
      console.log('Invalid credentials');
      alert('Invalid username or password');
    }
  };

  return (
    <div className="card">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Username:</label>
          <input 
            type="text" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div>
          <label>Password:</label>
          <input 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginCard;
