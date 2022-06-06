import { useState, useEffect } from "react";
import { Badge } from "react-bootstrap";

function BotChat(props) {
  const [response] = useState(props.response);
  const [buttonList, setButtonList] = useState([]);
  const [botResponse, setBotResponse] = useState("");

  const handleClick = (e) => {
    props.onButtonClick(e.target.innerText);
  };

  useEffect(() => {
    const list = response.split("[list]").filter((item, index) => {
      if (index > 0) {
        return true;
      }
      return false;
    });
    setButtonList(list);

    setBotResponse(response.split("[list]")[0]);
  }, [response]);

  return (
    <div className="mt-1 mb-1 bot-chat">
      <div>
        <Badge pill bg="warning" text="dark">
          bot &#10004;
        </Badge>{" "}
        {botResponse}
      </div>
      {buttonList.map((item, index) => {
        const button = item.split(",");
        return (
          <a href={button[1]} target="_blank" rel="noreferrer" key={index}>
            <Badge
              pill
              bg="info"
              className="chat-button"
              text="dark"
              style={{
                margin: "3px 5px 0 0",
              }}
              variant="outline-secondary"
              onClick={handleClick}
            >
              {button[0]}
            </Badge>
          </a>
        );
      })}
    </div>
  );
}

export default BotChat;
