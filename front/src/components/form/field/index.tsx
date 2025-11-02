import PasswordInput from "../password-input";

interface FormFieldProps {
  name: string;
  label: string;
  type: string;
  placeholder?: string;
  pattern?: string;
  title?: string;
  autocomplete?: string;

  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export default function FormField(props: FormFieldProps) {
  return (
    <div className="form-box">
      <label htmlFor={props.name}>{props.label}</label>

      {props.type === "password" ? (
        <PasswordInput
          name={props.name}
          value={props.value}
          onChange={props.onChange}
          placeholder={props.placeholder}
        />
      ) : (
        <input {...props} required />
      )}
    </div>
  );
}
