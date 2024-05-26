const QuestionTagPanel = () =>{
  return(
    <div>
      <Grid container spacing={2} style={{ padding: 20 }}>
        <Grid item xs={12} sm={4}>
          {tags.map(tag => (
            <TagCard
              key={tag}
              tag={tag}
              onClick={setSelectedTag}
              isSelected={tag === selectedTag}
            />
          ))}
        </Grid>
      </Grid>
      <Grid item xs={12} sm={8} style={{ maxHeight: '90vh', overflowY: 'auto' }}>
        <List>
          {questions.filter(q => !selectedTag || q.includes(selectedTag)).map((question, index) => (
            <ListItem key={index} button>
              <ListItemText primary={question} />
            </ListItem>
          ))}
        </List>
      </Grid>
    </div>
  );
};
export default QuestionTagPanel;