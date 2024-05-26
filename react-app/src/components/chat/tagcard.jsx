import { CardActionArea, CardContent, Typography, makeStyles } from "@mui/material";

const useStyles = makeStyles({
  card: {
    margin: 8,
  }
});

const TagCard = ({tag, onClick, isSelected}) => {
  const classes = useStyles();
  return (
    <Card className ={classes.card} onClick ={() => onClick(tag)} elevation={isSelected ? 3 : 1}>
      <CardActionArea>
        <CardContent>
          <Typography>
            {tag}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};
export default TagCard;