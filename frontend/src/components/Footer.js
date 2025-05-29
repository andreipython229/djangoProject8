// src/components/Footer.js

import { FaInstagram, FaTelegramPlane, FaPhoneAlt, FaEnvelope } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white text-sm py-6 mt-10">
      <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row justify-between items-center">
        <p className="mb-2 sm:mb-0">© 2025 DogShop. Все права защищены.</p>

        <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-6 text-center sm:text-left">
          <div className="mb-2 sm:mb-0">
            <a href="/contacts" className="hover:underline">Контакты</a> ·{" "}
            <a href="/about" className="hover:underline">О нас</a> ·{" "}
            <a href="/policy" className="hover:underline">Политика</a>
          </div>

          <div className="flex items-center justify-center space-x-4 mt-2 sm:mt-0">
            <a href="tel:+79991234567" className="hover:text-blue-400" title="Позвонить">
              <FaPhoneAlt />
            </a>
            <a href="mailto:info@dogshop.ru" className="hover:text-blue-400" title="Написать email">
              <FaEnvelope />
            </a>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:text-pink-500" title="Instagram">
              <FaInstagram />
            </a>
            <a href="https://t.me/dogshop" target="_blank" rel="noopener noreferrer" className="hover:text-blue-400" title="Telegram">
              <FaTelegramPlane />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
