import { useEffect, useRef } from "react";
import BotChat from "./BotChat";
import UserChat from "./UserChat";

function Chats(props) {
  const handleButtonClick = (text) => {
    props.onInputChange(text);
  };
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current.scrollIntoView({
      behavior: "smooth",
      block: "end",
      inline: "nearest",
    });
  }, [props.chats]);

  return (
    <div ref={chatRef}>
      {props.chats.map((item, index) =>
        item.isUser ? (
          <UserChat key={index} text={item.text} />
        ) : (
          <BotChat
            key={index}
            response={item.text}
            onButtonClick={handleButtonClick}
          />
        )
      )}
    </div>
  );
}

export default Chats;
