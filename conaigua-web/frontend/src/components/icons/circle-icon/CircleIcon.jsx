import "./CircleIcon.css";

export function CircleIcon ({ icon: Icon, variant, className, size}) {
  return (
    <div className={`circle-icon circle-icon--${variant} ${className}`}>
      <Icon size={size} />
    </div>
  );
};