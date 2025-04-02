import React, { useState } from 'react';
import axios from 'axios';

const NarrativeInput = () => {
    const [narrative, setNarrative] = useState('');
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [error, setError] = useState(null);

    const handleInputChange = (e) => {
        setNarrative(e.target.value);
    };

    const handleSaveNarrative = async () => {
        setLoading(true);
        setSuccess(false);
        setError(null);

        try {
            const response = await axios.post('/api/v1/narratives', { content: narrative });
            if (response.status === 200) {
                setSuccess(true);
            }
        } catch (err) {
            setError('Failed to save narrative. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Personal Narrative</h2>
            <textarea
                value={narrative}
                onChange={handleInputChange}
                placeholder="Write your personal narrative here..."
                rows="10"
                cols="50"
            />
            <button onClick={handleSaveNarrative} disabled={loading}>
                {loading ? 'Saving...' : 'Save Narrative'}
            </button>
            {success && <p>Narrative saved successfully!</p>}
            {error && <p>{error}</p>}
        </div>
    );
};

export default NarrativeInput;
