import { useState, useEffect } from 'react';

export default function AgentStatus() {

    const [agentStatus, setAgentStatus] = useState('');



    const checkAgentStatus = () => {
        const intervalId = setInterval(async () => {
            try {
                const res = await fetch('http://localhost:8000/status', {
                    method: 'POST'
                });
                const data = await res.json();
                setAgentStatus(data);

                if (data.status === 'Done') {
                    setAgentStatus('');
                    clearInterval(intervalId); // Clear interval when status is "Done"
                }
            } catch (error) {
                console.error('Error fetching status:', error);
            }
        }, 750); // 0.75 seconds

        return intervalId;
    };

    useEffect(() => {
        const intervalId = checkAgentStatus();

        return () => {
            clearInterval(intervalId); // Clear interval when component unmounts
        };
    }, [])

    return (

        <div>
            {agentStatus}
        </div>


    )
}