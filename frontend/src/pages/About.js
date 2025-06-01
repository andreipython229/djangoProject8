import '../css/About.css';
import dogImage from '../assets/img/pexels-didsss-1383813.jpg';

export default function About() {
  return (
    <div className="about">
      <h2 className="about-title">О нас</h2>
      <div className="about-image-container">
        <img src={dogImage} alt="Собака" className="about-image" />
      </div>
    </div>
  );
}
