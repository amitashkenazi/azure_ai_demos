from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

def fine_tune_model(model_path, jsonl_file_path, training_args):
    # Load a pre-trained model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # Load dataset from JSONL file
    dataset = load_dataset('json', data_files=jsonl_file_path)


    def tokenize_function(examples):
        model_inputs = tokenizer(examples['heb'], max_length=128, truncation=True)
        # Setup the tokenizer for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(examples['arc'], max_length=128, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_dataset = dataset.map(tokenize_function, batched=True)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=8,  # Reduced batch size
        gradient_accumulation_steps=2,  # Gradient accumulation
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        evaluation_strategy="steps",
        eval_steps=500,
        fp16=True,  # Enable mixed precision training
        dataloader_num_workers=2  # Limit number of CPU threads
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        # eval_dataset=val_dataset,
    )

    # Train the model
    trainer.train()

# Example usage
fine_tune_model("mistralai-Mistral-7B-v0.1", "data/all_captions_1704098839_part2.jsonl", TrainingArguments)
