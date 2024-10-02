import React from 'react';
import Slider from 'react-slick';
import LoginCard from './LoginCard';
import SignupCard from './SignupCard';
import './App.css';
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";

const App = () => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 800, /* Adjust speed for smoother transition */
    slidesToShow: 1,
    slidesToScroll: 1,
    fade: false, /* You can enable fade transition if preferred */
    cssEase: "ease-in-out", /* For smooth easing */
  };

  return (
    <div className="app-container">
      <div className="background-image"></div>
      <h1 className="maintitle">
        Web pentest report summarizer
      </h1>
      <Slider {...settings} className="slider">
        <div>
          <LoginCard />
        </div>
        <div>
          <SignupCard />
        </div>
      </Slider>
    </div>
  );
};

export default App;
