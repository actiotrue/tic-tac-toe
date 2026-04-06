package client

import (
	"log"
	"time"

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

const (
    pongWait = 300 * time.Second 
    
    pingPeriod = (pongWait * 9) / 10
)


func (c *Client) WritePump() {
	ticker := time.NewTicker(pingPeriod)
	defer func() {
		ticker.Stop()
		c.Conn.Close()
	}()

	for {
		select {
		case message, ok := <-c.Send:
			c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if !ok {
				c.Conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			if err := c.Conn.WriteMessage(websocket.TextMessage, message); err != nil {
				return
			}
		case <-ticker.C:
			c.Conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
			if err := c.Conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}

func (c *Client) ReadPump() {
	defer func() {
		c.Done <- c
		c.Conn.Close()
	}()
	c.Conn.SetReadLimit(512)
    c.Conn.SetReadDeadline(time.Now().Add(pongWait))
	    c.Conn.SetPongHandler(func(string) error { 
        c.Conn.SetReadDeadline(time.Now().Add(pongWait))
        return nil 
    })
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
