import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

import styles from './MPVoting.module.css';


interface MPVotingProps {
    memberId: string;
}
interface Vote {
    member_id: number;
    division_id: number;
    date: string;
    title: string;
    member_voted_aye: number;
    member_was_teller: number;
}

const MPVoting: React.FC = () => {
    const [votes, setVotes] = useState<any[]>([]);
    const { memberId } = useParams<{ memberId: string }>();
    const { voteType } = useParams<{ voteType: string }>();

    const fetchVotes = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/members/${memberId}/votes/${voteType}`);
            const data = await response.json();
            console.log('data:', data);
            setVotes(data);
        } catch (error) {
            console.error('Error fetching votes data:', error);
        }
    };

    useEffect(() => {
        fetchVotes();
    }, [memberId]);

    return (
        <div className={styles.container}>
            <h2 className={styles.title}>Votes by Member ID: {memberId}</h2>
            <ul className={styles.voteList}>
                {votes.map((vote) => (
                    <li key={vote.division_id} className={styles.voteItem}>
                        <span>
                            {vote.date}: {vote.title}
                            <span className={styles.voteDate}>({new Date(vote.date).toLocaleDateString()})</span>
                        </span>
                        <span>{vote.member_voted_aye ? 'Yes' : 'No'}</span>
                    </li>
                ))}
            </ul>
        </div>

    );
};

export default MPVoting;
