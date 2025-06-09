import React from 'react';

const AdCard = ({ ad }) => {
  // L'URL de l'image doit être construite en préfixant l'URL de l'API
  const imageUrl = `http://127.0.0.1:8000/${ad.image_url.replace(/\\/g, '/')}`;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300">
      <img src={imageUrl} alt={ad.title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-lg font-bold">{ad.title}</h3>
        <p className="text-gray-600 mt-1 truncate">{ad.description}</p>
        <div className="mt-4 flex justify-between items-center">
          <p className="text-xl font-bold text-blue-600">${ad.price.toFixed(2)}</p>
          <button className="bg-blue-500 text-white text-sm font-bold py-1 px-3 rounded hover:bg-blue-600">
            Voir
          </button>
        </div>
      </div>
    </div>
  );
};

export default AdCard;