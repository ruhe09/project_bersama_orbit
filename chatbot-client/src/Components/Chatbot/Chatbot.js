import { useEffect, useState } from "react";
import { InputGroup, Button, FormControl, Badge } from "react-bootstrap";
import Chats from "./Chats";
import "./Chatbot.css";

function Chatbot() {
  const [input, setInput] = useState("");
  const [shoudSubmit, setShouldSubmit] = useState(false);
  const [chats, setChats] = useState([]);
  const [show, setShow] = useState(true);
  const [isOnline, setIsOnline] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    testConnection();
    const msg = input;
    const res = await fetch("https://127.0.0.1:5000/chatbot?msg=" + msg);
    const data = await res.json();
    setChats([
      ...chats,
      {
        text: input,
        isUser: true,
      },
      {
        text: data.response,
        isUser: false,
      },
    ]);
    setInput("");
    setLoading(false);
  };

  const handleInputChange = (text) => {
    setInput(text);
    setShouldSubmit(true);
  };

  useEffect(() => {
    document.getElementById("submit").click();
    setShouldSubmit(false);
  }, [shoudSubmit]);

  const testConnection = async () => {
    try {
      const res = await fetch("https://127.0.0.1:5000/chatbot?msg=hello");
      const data = await res.json();
      if (data.response) {
        setIsOnline(true);
      } else {
        setIsOnline(false);
      }
    } catch (error) {
      setIsOnline(false);
    }
  };

  if (show) {
    return (
      <div className="m-3 chatbot">
        <div>
          {/* header section */}
          <h5 className="chat-header pt-1 pb-2">
            <strong style={{ color: "#fff", position: "relative", top: "2px" }}>
              chatbot
            </strong>{" "}
            <Badge bg={isOnline ? "success" : "danger"}>
              {isOnline ? "online" : "offline"}
            </Badge>{" "}
          </h5>
          <div
            className="close-button"
            onClick={(e) => setShow(!show)}
            bg="danger"
          >
            <box-icon name="x" color="#ffffff"></box-icon>
          </div>{" "}
          {/* chats section */}
          <div className="chats-container">
            <Chats chats={chats} onInputChange={handleInputChange} />
          </div>
          <form onSubmit={handleSubmit} className="mt-3 chat-container">
            <InputGroup className="mb-3">
              <FormControl
                placeholder="Message..."
                aria-label="Message..."
                aria-describedby="basic-addon2"
                name="msg"
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />
              <Button type="submit" variant="primary" id="submit">
                <box-icon
                  name="paper-plane"
                  color="#ffffff"
                  style={{
                    position: "relative",
                    top: "2px",
                    right: "1px",
                  }}
                ></box-icon>
              </Button>
            </InputGroup>
          </form>
        </div>
        <div
          className="bot-typing"
          style={{
            display: loading ? "unset" : "none",
          }}
        >
          Bot is typing...
        </div>
      </div>
    );
  } else {
    return (
      <div className="toggle-button">
        <box-icon
          onClick={(e) => setShow(!show)}
          type="logo"
          name="messenger"
          size="lg"
          color="#ffffff"
        ></box-icon>
      </div>
    );
  }
}

export default Chatbot;
