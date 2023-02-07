class MessageParser {
    constructor(actionProvider, state) {
      this.actionProvider = actionProvider;
      console.log(this.actionProvider);
      this.state = state;
    }
  
    parse(message) {
      let botMessage = this.actionProvider.createChatBotMessage(message);
      this.actionProvider.setState((prev, props) => ({
          ...prev,
          messages: [...prev.messages, botMessage]
      }))
    }
  }

export default MessageParser;
