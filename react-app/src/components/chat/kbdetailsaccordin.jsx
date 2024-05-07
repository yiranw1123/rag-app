import React from 'react';
import Accordion from '@mui/material/Accordion';
import AccordionSummary from '@mui/material/AccordionSummary';
import AccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import { useSelector } from 'react-redux';


export default function DetailsAccordion() {
  const files = useSelector(state => state.chat.kbFiles);
  const kbDetails = useSelector(state => state.chat.selectedKB)
  console.log(kbDetails);

  return (
    <div>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Knowledgebase Details</Typography>
        </AccordionSummary>
        <AccordionDetails>
        <List component="nav" aria-label="Knowledge base details">
            <ListItem divider>
              <ListItemText primary="Name" secondary={kbDetails.name} />
            </ListItem>
            <ListItem divider>
              <ListItemText primary="ID" secondary={kbDetails.id} />
            </ListItem>
            <ListItem divider>
              <ListItemText primary="Embedding" secondary={kbDetails.embedding} />
            </ListItem>
            <ListItem divider>
              <ListItemText primary="Created" secondary={kbDetails.created} />
            </ListItem>
            <ListItem divider>
              <ListItemText primary="Updated" secondary={kbDetails.updated} />
            </ListItem>
            <ListItem divider>
              <ListItemText primary="Description" secondary={kbDetails.description || "No description provided."} />
            </ListItem>
          </List>
        </AccordionDetails>
      </Accordion>
      <Accordion>
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1a-content"
          id="panel1a-header"
        >
          <Typography>Knowledgebase Files</Typography>
        </AccordionSummary>
        <AccordionDetails>
          <List component="nav" aria-label="mailbox folders">
            {files?.map((file, index) => (
              <ListItem key={file.id} divider>
                <ListItemText primary={file.file_name || 'Unknown'} secondary={file.created || 'No date'} />
              </ListItem>
            ))}
          </List>
        </AccordionDetails>
      </Accordion>
    </div>
  );
}
