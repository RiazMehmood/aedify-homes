const FloatingAIChat = () => {
  return (
    <div className="bg-white shadow-lg rounded-xl p-4">
      <h3 className="text-md font-semibold mb-2">💬 AI Assistant</h3>
      <p className="text-sm text-gray-600 mb-3">
        Ask me: <br />
        “Best rent for 2-bed flat in Lahore”<br />
        “Improve my listing”<br />
        “Show complaints”
      </p>
      <button className="bg-blue-600 text-white text-sm py-2 px-4 rounded-lg w-full">
        Open Chat
      </button>
    </div>
  );
};

export default FloatingAIChat;
