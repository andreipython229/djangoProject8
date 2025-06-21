import dogImage from '../assets/img/pexels-didsss-1383813.jpg';

export default function About() {
  return (
    <div className="about">
      <h2 className="about-title">О нашем проекте</h2>
      <div className="about-image-container">
        <img src={dogImage} alt="Собака" className="about-image" />
      </div>
      <div className="about-text-container">
        <p>
          Добро пожаловать в <strong>Bestdogs</strong> — лучший ресурс для любителей собак! 
          Наш проект создан с целью объединить всех, кто не представляет свою жизнь без четвероногих друзей.
        </p>
        <p>
          Здесь вы можете делиться фотографиями своих питомцев, находить информацию о породах, 
          а также открывать для себя новые места для прогулок, которые будут интересны и вам, и вашей собаке.
        </p>
        <p>
          Мы верим, что каждая собака заслуживает любви и заботы. Присоединяйтесь к нашему сообществу!
        </p>
      </div>
    </div>
  );
}
