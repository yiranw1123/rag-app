import React, {useState, useEffect} from "react";

import useTable from '../hooks/useTable';
import TableFooter from "./TableFooter/tablefooter";
import styles from "./Table.module.css";

const DetailsTable = ({data, rowsPerPage, kbId, onBack}) => {

  const [page, setPage] = useState(1);
  const {slice, range} = useTable(data, page, rowsPerPage);
  
  return(
    <>
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
        {slice.map((file) => (
          <tr key={file.id} className={styles.tableRowHeader}>
            <td className={styles.tableCell}>{file.id}</td>
            <td className={styles.tableCell}>{file.name}</td>
            <td className={styles.tableCell}>{file.created}</td>
            <td className={styles.tableCell}>{file.updated}</td>
            <td className={`${styles.tableCell} ${styles.buttonContainer}`}>
              <button className={`${styles.actionButton} ${styles.deleteButton}`}> Delete</button>
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