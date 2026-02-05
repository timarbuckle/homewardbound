from google.cloud import storage
import sys

def verify_storage(bucket_name):
    try:
        # This automatically uses the VM's Service Account
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        
        # Try to list the first 5 blobs
        print(f"✅ Success! Connected to bucket: {bucket_name}")
        blobs = list(bucket.list_blobs(max_results=5))
        print(f"Found {len(blobs)} files in bucket.")
        
    except Exception as e:
        print(f"❌ Connection Failed!")
        print(f"Error: {e}")
        print("\nChecklist:")
        print("1. Is the bucket name spelled correctly?")
        print("2. Does the Service Account have 'Storage Object Viewer' or 'Admin'?")
        print("3. Is the VM 'Access Scope' set to 'Allow Full Access'?")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run verify_storage.py bucket-name")
    else:
        verify_storage(sys.argv[1])
