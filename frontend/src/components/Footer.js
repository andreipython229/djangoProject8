// src/components/Footer.js

import { Link } from 'react-router-dom';
import { FaInstagram, FaTelegramPlane, FaPhoneAlt, FaEnvelope } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-dark text-white py-4 mt-5">
      <div className="container d-flex flex-column flex-sm-row justify-content-between align-items-center text-center text-sm-start">
        <p className="mb-2 mb-sm-0">© 2025 DogShop. Все права защищены.</p>
        <div className="d-flex flex-column flex-sm-row align-items-center gap-3">
          <div>
            <Link to="/contacts" className="text-white text-decoration-none me-2">Контакты</Link>
            <Link to="/about" className="text-white text-decoration-none me-2">О нас</Link>
            <Link to="/policy" className="text-white text-decoration-none">Политика</Link>
          </div>
          <div className="d-flex align-items-center gap-3">
            <a href="tel:+375291272646" className="text-white" title="Позвонить">
              <FaPhoneAlt className="footer-icon" />
            </a>
            <a href="mailto:panbbbqv@gmail.com" className="text-white" title="Написать на Email">
              <FaEnvelope className="footer-icon" />
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="text-white" title="Instagram">
              <FaInstagram className="footer-icon" />
            </a>
            <a href="https://t.me/dogshop" target="_blank" rel="noopener noreferrer" className="text-white" title="Telegram">
              <FaTelegramPlane className="footer-icon" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}