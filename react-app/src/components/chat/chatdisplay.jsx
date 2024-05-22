import { useDispatch, useSelector } from "react-redux";

const ChatDisplay = () => {
  const chatId = useSelector(state => state.chat.chatId);
  const dispatch = useDispatch();

  useEffect(() => {
    // call backend to get prev questions on first render
    dispatch(fetchQuestions(chatId));
  }, [dispatch, chatId]);

};
export default ChatDisplay;