const API_BASE_URL = '/api/v1';

export async function fetchMyDogs() {
  const token = localStorage.getItem('access');
  console.log('Токен для запроса:', token);
  if (!token) throw new Error('Нет токена авторизации');

  const response = await fetch(`${API_BASE_URL}/mydogs/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error('Ошибка при загрузке списка собак');
  }

  return await response.json();
}