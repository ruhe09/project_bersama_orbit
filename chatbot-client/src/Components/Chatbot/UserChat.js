function UserChat(props) {
  if (props.text === "") {
    return null;
  } else {
    return (
      <div className="user-chat">
        <div className="user-chat-text">{props.text}</div>
        <div className="user-chat-addon"></div>
      </div>
    );
  }
}

export default UserChat;
