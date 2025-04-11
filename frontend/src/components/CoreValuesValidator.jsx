import React from 'react';

/**
 * CoreValuesValidator - UI validation component that verifies alignment with ThinkAlike's ethical principles
 * 
 * This component is part of ThinkAlike's "UI as Validation Framework" and provides visual feedback
 * on how well a specific action, data processing step, or AI output aligns with core ethical values.
 * 
 * @param {Object} props.validationContext - The context of what's being validated (e.g., API call, data, recommendation)
 * @param {Object} props.validationResults - Optional pre-computed validation results
 * @param {string} props.displayMode - 'compact' or 'detailed' view
 */
const CoreValuesValidator = ({ validationContext, validationResults, displayMode = 'compact' }) => {
  const [results, setResults] = React.useState(validationResults);
  const [isLoading, setIsLoading] = React.useState(!validationResults && validationContext);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    // If validation results aren't provided but context is, fetch from backend
    if (!validationResults && validationContext) {
      setIsLoading(true);
      // Mock API call - would be replaced with actual service call
      setTimeout(() => {
        setResults({
          overallScore: 85,
          principles: {
            transparency: 'ok',
            userControl: 'ok', 
            dataMinimization: 'warning',
            biasProtection: 'ok'
          },
          concerns: [
            {
              severity: 'Medium',
              description: 'Collecting more user data than strictly necessary for this operation',
              recommendation: 'Review fields being requested and limit to essential ones'
            }
          ]
        });
        setIsLoading(false);
      }, 500);
    } else {
      setResults(validationResults);
    }
  }, [validationContext, validationResults]);

  const getStatusColor = (score) => {
    if (score >= 80) return 'green';
    if (score >= 60) return 'amber';
    return 'red';
  };

  if (isLoading) return <div className="coreValuesValidator loading">Validating ethical alignment...</div>;
  if (error) return <div className="coreValuesValidator error">Error validating ethics: {error.message}</div>;
  if (!results) return null;

  return (
    <div className={`core-values-validator mode-${displayMode}`}>
      <div className={`ethical-score status-${getStatusColor(results.overallScore)}`}>
        <span className="score-label">Ethical Alignment:</span>
        <span className="score-value">{results.overallScore}%</span>
      </div>

      {displayMode === 'detailed' && (
        <>
          <div className="principle-breakdown">
            <h4>Principle Check:</h4>
            <ul>
              {Object.entries(results.principles || {}).map(([principle, status]) => (
                <li key={principle} className={`status-${status}`}>
                  {principle}: {status.toUpperCase()}
                </li>
              ))}
            </ul>
          </div>

          {results.concerns && results.concerns.length > 0 && (
            <div className="concerns-log">
              <h4>Identified Concerns:</h4>
              <ul>
                {results.concerns.map((concern, index) => (
                  <li key={index} className={`severity-${concern.severity.toLowerCase()}`}>
                    [{concern.severity}] {concern.description}
                    {concern.recommendation && (
                      <div className="recommendation">Recommendation: {concern.recommendation}</div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CoreValuesValidator;
