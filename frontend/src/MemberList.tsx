import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import styles from './MemberList.module.css';

interface MemberListProps {
  searchTerm: string;
}

interface Member {
  created_at: string;
  gender: 'M' | 'F' | 'U';
  house: number;
  id: number;
  latestPartyAbbreviation: string;
  latestPartyBackgroundColour: string;
  latestPartyForegroundColour: string;
  latestPartyGovernmentType: number;
  latestPartyId: number;
  latestPartyIsIndependentParty: number;
  latestPartyIsLordsMainParty: number;
  latestPartyIsLordsSpiritualParty: number;
  latestPartyName: string;
  member_id: number;
  membershipEndDate: string | null;
  membershipEndReason: string | null;
  membershipEndReasonId: number | null;
  membershipEndReasonNotes: string | null;
  membershipFrom: string;
  membershipFromId: number;
  membershipStartDate: string;
  membershipStatus: number;
  membershipStatusDescription: string;
  membershipStatusId: number;
  membershipStatusIsActive: number;
  membershipStatusNotes: string | null;
  membershipStatusStartDate: string;
  nameAddressAs: string;
  nameDisplayAs: string;
  nameFullTitle: string;
  nameListAs: string;
  thumbnailUrl: string;
}

const MemberList: React.FC<MemberListProps> = ({ searchTerm }) => {
  const [members, setMembers] = useState<Member[]>([]);

  const fetchMembers = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/members');
      const data = await response.json();
      console.log('data:', data);
      setMembers(data);
    } catch (error) {
      console.error('Error fetching members data:', error);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, []);

  return (
    <div className={styles.container}>
      {members.filter((member) =>
        member.nameFullTitle.toLowerCase().includes(searchTerm.toLowerCase())
      )
        .map((member) => (
          <div key={member.id} className={styles.card}>
            <img
              src={member.thumbnailUrl}
              alt={member.nameFullTitle}
              className={styles.thumbnail}
            />
            <div className={styles.overlay}>
              <h3 className={styles.title}>{member.nameFullTitle}</h3>
              <p className={styles.party}>{member.latestPartyName}</p>
              <p className={styles.from}>From: {member.membershipFrom}</p>
              <Link to={`/mp/${member.member_id}/votes/1`}>
                <button>See Yes Votes</button>
              </Link>
              <Link to={`/mp/${member.member_id}/votes/0`}>
                <button>See No Votes</button>
              </Link>
            </div>

          </div>
        ))}
    </div>
  );
};

export default MemberList;
