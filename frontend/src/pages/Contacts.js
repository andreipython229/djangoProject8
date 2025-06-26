import React from 'react';

const Contacts = () => {
  return (
    <div className="min-h-screen bg-white text-center py-16 px-4">
      <h1 className="text-4xl font-bold text-gray-900 mb-6">Контакты</h1>
      <p className="text-lg text-gray-700 mb-4">
        Свяжитесь с нами по любым вопросам, связанным с нашими собаками.
      </p>
      <div className="text-md text-gray-600 space-y-2">
        <p>📞 Телефон: +375291272646</p>
        <p>
          📧 Email: <a href="mailto:panbbbqv@gmail.com" className="text-blue-600 underline">panbbbqv@gmail.com</a>
        </p>
        <p>📍 Адрес: г. Москва, ул. Лапкина, д. 42</p>
      </div>
    </div>
  );
};

export default Contacts;