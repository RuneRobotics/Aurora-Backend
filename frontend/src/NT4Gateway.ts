export class NT4Gateway {
  public serverUrl: string;
  public socket: WebSocket | null = null;

  constructor(serverUrl: string) {
    this.serverUrl = serverUrl;
  }

  connect() {
    this.socket = new WebSocket(this.serverUrl);

    this.socket.onopen = () => {
      console.log("Connected to NT4 server");
      this.send({ type: "subscribe", topics: ["example_table/example_data"] });
    };

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.socket.onclose = () => {
      console.log("Connection closed");
    };

    this.socket.onerror = (err) => {
      console.error("WebSocket error:", err);
    };
  }

  send(message: object) {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(message));
    }
  }

  handleMessage(message: any) {
    console.log("Received message:", message);
    // Add logic to handle incoming data
  }

  publish(topic: string, value: any) {
    this.send({
      type: "publish",
      topic: topic,
      value: value,
    });
  }

  close() {
    if (this.socket) {
      this.socket.close();
    }
  }
}
