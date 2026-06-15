/**
 * CDK Exercise 01 — Stack Basics: the "StorageStack" pattern
 * ============================================================
 *
 * CONCEPTS:
 *   - cdk.Stack          → one CloudFormation stack. constructor(scope, id, props).
 *   - cdk.StackProps     → base props (env, stackName, tags...) — extend it with
 *                          whatever YOUR stack needs from the caller.
 *   - cdk.App            → root container. `new App()`, then `new XStack(app, 'Id', props)`.
 *   - readonly exported properties → how OTHER stacks reference this stack's
 *                          resources (cross-stack references). CDK turns these
 *                          into CloudFormation Fn::ImportValue / Outputs automatically.
 *   - s3.Bucket (L2)     → sensible defaults + helper methods (grantRead, grantWrite...).
 *   - cdk.RemovalPolicy  → DESTROY (dev — delete on `cdk destroy`) vs RETAIN (prod).
 *   - cdk.CfnOutput      → printed after `cdk deploy`, visible in the CFN console.
 *
 * REAL-WORLD REFERENCE:
 *   This mirrors lib/storage-stack.ts in aws-etl-pipeline-cdk — the simplest stack
 *   in that app: 3 S3 buckets (raw, processed, scripts), each exposed as a
 *   `readonly` property so GlueStack / SageMakerStack can take them as props.
 *   This is "Stack 1" — no dependencies, deployed first.
 *
 * RUN:
 *   cd typescript/cdk && npm install   (one-time — installs aws-cdk-lib + constructs)
 *   npx tsx exercises/01_storage_stack.ts
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Template } from 'aws-cdk-lib/assertions';

// ---- EXAMPLE (for reference) ----
//
// A minimal stack with ONE bucket and no extra props. Note the shape:
//   1. interface ...Props extends cdk.StackProps   (even if empty — convention)
//   2. class ...Stack extends cdk.Stack
//   3. constructor(scope, id, props) { super(scope, id, props); ... }
//   4. readonly properties for anything other stacks might need
class LogsStack extends cdk.Stack {
  readonly logsBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.logsBucket = new s3.Bucket(this, 'LogsBucket', {
      removalPolicy:     cdk.RemovalPolicy.DESTROY,   // dev only
      autoDeleteObjects: true,                        // dev only — lets `cdk destroy` actually empty the bucket
    });

    new cdk.CfnOutput(this, 'LogsBucketName', { value: this.logsBucket.bucketName });
  }
}

// ---- TASK 1: Build `StorageStack` with three buckets ----
//
// interface StorageStackProps extends cdk.StackProps {}   (no inputs — Stack 1, deployed first)
//
// class StorageStack extends cdk.Stack {
//   readonly rawBucket:       s3.Bucket;
//   readonly processedBucket: s3.Bucket;
//   readonly scriptsBucket:   s3.Bucket;
//
//   constructor(scope, id, props) { ... }
// }
//
// Requirements:
//   - rawBucket:       versioned: true, removalPolicy DESTROY, autoDeleteObjects true
//   - processedBucket: versioned: true, removalPolicy DESTROY, autoDeleteObjects true,
//                       PLUS a lifecycle rule that transitions objects to
//                       INFREQUENT_ACCESS storage class after 30 days
//                       (use `lifecycleRules: [{ transitions: [{ storageClass: ..., transitionAfter: cdk.Duration.days(30) }] }]`)
//   - scriptsBucket:   versioned: false, removalPolicy DESTROY, autoDeleteObjects true
//   - Assign each bucket to a `readonly` property so a future GlueStack could take
//     them as props (like Exercise 02 does)
//   - Add a CfnOutput for each bucket's name

// YOUR CODE HERE

interface StorageStackProps extends cdk.StackProps {
  // ...
}

class StorageStack extends cdk.Stack {
  // readonly rawBucket: s3.Bucket;
  // readonly processedBucket: s3.Bucket;
  // readonly scriptsBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props?: StorageStackProps) {
    super(scope, id, props);

    // ...
  }
}

// ---- TASK 2: Instantiate it ----
//
// Create a `cdk.App`, then `new StorageStack(app, 'TestStorage')`.
// (No `env` needed for this exercise — synth works fine without an account/region.)

// YOUR CODE HERE
// const app = new cdk.App();
// const storage = new StorageStack(app, 'TestStorage');

// ---- TESTS ---- (uncomment after implementing)
//
// Template.fromStack(...) renders the synthesized CloudFormation template.
// hasResourceProperties / resourceCountIs THROW (with a helpful diff) if the
// assertion fails — that thrown error IS your test failure message.

/*
const template = Template.fromStack(storage);

// 3 buckets total
template.resourceCountIs('AWS::S3::Bucket', 3);

// versioning enabled on raw + processed (but not scripts)
template.hasResourceProperties('AWS::S3::Bucket', {
  VersioningConfiguration: { Status: 'Enabled' },
});

// processed bucket has a lifecycle rule transitioning to STANDARD_IA after 30 days
template.hasResourceProperties('AWS::S3::Bucket', {
  LifecycleConfiguration: {
    Rules: [
      {
        Transitions: [
          { StorageClass: 'STANDARD_IA', TransitionInDays: 30 },
        ],
      },
    ],
  },
});

console.log('✓ 01_storage_stack — all tests passed');
*/

void LogsStack; // suppress unused-variable lint for the EXAMPLE class
