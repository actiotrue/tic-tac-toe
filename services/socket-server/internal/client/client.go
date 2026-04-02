package client

import (
	"log"

	"github.com/gorilla/websocket"
)

type Message struct {
	Client *Client
	Data   []byte
}

type Client struct {
	UserId   string
	Conn     *websocket.Conn
	Send     chan []byte
	Incoming chan Message
	Done     chan *Client
}

func (c *Client) WritePump() {
	for msg := range c.Send {
		err := c.Conn.WriteMessage(websocket.TextMessage, msg)
		if err != nil {
			log.Println("Error while sending message: ", err)
			break
		}
	}
}

func (c *Client) ReadPump() {
	defer func() {
		c.Done <- c
		c.Conn.Close()
	}()
	for {
		_, message, err := c.Conn.ReadMessage()
		if err != nil {
			log.Println("Error while reading message: ", err)
			return
		}
		c.Incoming <- Message{
			Client: c,
			Data:   message,
		}
	}
}
