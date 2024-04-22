import React, {useState} from "react";

import useTable from '../hooks/useTable';
import TableFooter from "./tablefooter";
import styles from "./Table.module.css";

const DetailsTable = ({data, rowsPerPage, kbId, onDelete, onBack}) => {

  const [page, setPage] = useState(1);
  const {slice, range} = useTable(data, page, rowsPerPage);
  
  return(
    <>
    <h2>All files for KnowldegeBase with id: {kbId}</h2>
    <table className={styles.table}>
      <thead className={styles.tableRowHeader}>
        <tr>
          <th className={styles.tableHeader}>Id</th>
          <th className={styles.tableHeader}>FileName</th>
          <th className={styles.tableHeader}>Created</th>
          <th className={styles.tableHeader}>Last Updated</th>
          <th className={styles.tableHeader}>Actions</th>
        </tr>
      </thead>
      <tbody>
        {slice.map((file, index) => (
          <tr key={file.id} className={styles.tableRowHeader}>
            <td className={styles.tableCell}>{index+1}</td>
            <td className={styles.tableCell}>{file.file_name}</td>
            <td className={styles.tableCell}>{file.created}</td>
            <td className={styles.tableCell}>{file.updated}</td>
            <td className={`${styles.tableCell} ${styles.buttonContainer}`}>
              <button className={`${styles.actionButton} ${styles.deleteButton}`} onClick={() => onDelete(file.id, kbId)}> Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    <TableFooter range={range} slice={slice} setPage={setPage} page={page}/>
    <button className='btn btn-primary' onClick={onBack}>Back to All KnowledgeBase</button>
  </>
  );

};
export default DetailsTable;