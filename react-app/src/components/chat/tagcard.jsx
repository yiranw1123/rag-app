import { Card, CardActionArea, Typography } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { toggleTag, getSelectedTags } from "../../features/tagState";

const TagCard = ({ tag }) => {
  const dispatch = useDispatch();
  const selectedTags = useSelector(getSelectedTags);
  const isSelected = selectedTags.includes(tag);

  const handleClick = () => {
    dispatch(toggleTag(tag));
  };

  return (
    <Card 
      sx={{
        mb: 2, 
        backgroundColor: isSelected ? 'secondary.main' : 'background.paper',
        '&:hover': {
          backgroundColor: 'primary.light',
          cursor: 'pointer'
        }
      }}
      style={{
        margin: '2px',  // Add more space around each card if needed
        padding: '3px', // Ensure internal padding doesn't affect layout
        border: '1px solid #ccc', // Example border for visual separation
        borderRadius: '5px'  // Optional for aesthetic
      }}
      onClick={handleClick}
    >
      <CardActionArea>
        <Typography sx={{ p: 1 }}>
          {tag}
        </Typography>
      </CardActionArea>
    </Card>
  );
};
export default TagCard;