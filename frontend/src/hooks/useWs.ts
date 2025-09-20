import { useEffect, useRef } from 'react';
import { useChat as useChatContext } from '../context/ChatContext';
import { useAuth } from './useAuth';

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL;

export function useChatWS() {
  const wsRef = useRef<WebSocket | null>(null);
  const { state: token } = useAuth();
  const { dispatch } = useChatContext();

  useEffect(() => {
    const ws = new WebSocket(`${WS_BASE_URL}/ws/me?token=${token.token}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
        console.log(event);
        const data = JSON.parse(event.data);

        switch (data.event) {
            case 'message_created':
                dispatch({ type: 'ADD_MESSAGE', payload: data.data.message });
            break;

            case 'message_updated':
                dispatch({ type: 'UPDATE_MESSAGE', payload: data.data.message });
            break;

            case 'message_deleted':
                console.log(data.data);
                dispatch({
                    type: 'DELETE_MESSAGE',
                    payload: { chatId: data.data.chat_id, messageId: data.data.message_id },
                });
            break;

            default:
            console.warn('Unknown WS event type:', data.type);
        }
    };

    ws.onclose = () => console.log('WebSocket closed');

    //return () => ws.close();
  }, [token]);

  return;
}
