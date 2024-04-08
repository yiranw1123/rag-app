import React, {useState} from "react";

import useTable from '../hooks/useTable';
import TableFooter from "./tablefooter";
import styles from "./Table.module.css";

const KBTable = ({data, rowsPerPage, onView, onDelete}) => {
  const [page, setPage] = useState(1);
  const {slice, range} = useTable(data, page, rowsPerPage);

  return(
    <>
      <table className={styles.table}>
        <thead className={styles.tableRowHeader}>
          <tr>
            <th className={styles.tableHeader}>Id</th>
            <th className={styles.tableHeader}>Name</th>
            <th className={styles.tableHeader}>Embedding</th>
            <th className={styles.tableHeader}>Created</th>
            <th className={styles.tableHeader}>Last Updated</th>
            <th className={styles.tableHeader}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {slice.map((knowledgebase) => (
            <tr key={knowledgebase.id} className={styles.tableRowHeader}>
              <td className={styles.tableCell}>{knowledgebase.id}</td>
              <td className={styles.tableCell}>{knowledgebase.name}</td>
              <td className={styles.tableCell}>{knowledgebase.embedding}</td>
              <td className={styles.tableCell}>{knowledgebase.created}</td>
              <td className={styles.tableCell}>{knowledgebase.updated}</td>
              <td className={`${styles.tableCell} ${styles.buttonContainer}`}>
                <button className={`${styles.actionButton} ${styles.viewButton}`} onClick={() => onView(knowledgebase.id)}> View</button>
                <button className={`${styles.actionButton} ${styles.deleteButton}`} onClick={() => onDelete(knowledgebase.id)}> Delete</button>
                <button className={`${styles.actionButton} ${styles.chatButton}`}> Chat</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <TableFooter range={range} slice={slice} setPage={setPage} page={page}/>
    </>
  );
};

export default KBTable;