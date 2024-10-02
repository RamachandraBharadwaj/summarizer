import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import Slider from "react-slick";
import LoginCard from "./LoginCard";
import SignupCard from "./SignupCard";
import Dashboard from "./Dashboard";
import DashboardLayout from "./DashboardLayout";
import "./App.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check if the user is logged in on component mount
  useEffect(() => {
    const checkLoginStatus = () => {
      const loggedIn = localStorage.getItem("isLoggedIn");
      if (loggedIn === "true") {
        setIsLoggedIn(true);
      }
    };
    checkLoginStatus();
  }, []);

  const settings = {
    dots: true,
    infinite: true,
    speed: 800,
    slidesToShow: 1,
    slidesToScroll: 1,
    fade: false,
    cssEase: "ease-in-out",
  };

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
    localStorage.setItem("isLoggedIn", "true");
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem("isLoggedIn");
  };

  return (
    <Router>
      <div className={`app-container ${!isLoggedIn ? "login-signup" : "dashboard"}`}>
        <Routes>
          {/* Login and Signup page with background */}
          {!isLoggedIn ? (
            <Route
              path="/"
              element={
                <Slider {...settings} className="slider">
                  <div>
                    <LoginCard onLoginSuccess={handleLoginSuccess} />
                  </div>
                  <div>
                    <SignupCard />
                  </div>
                </Slider>
              }
            />
          ) : (
            <Route path="/" element={<Navigate to="/dashboard" />} />
          )}

          {/* Dashboard page with DashboardLayout */}
          <Route
            path="/dashboard"
            element={
              isLoggedIn ? (
                <DashboardLayout handleLogout={handleLogout}>
                  <Dashboard />
                </DashboardLayout>
              ) : (
                <Navigate to="/" />
              )
            }
          />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
