/**
 * CDK Exercise 02 — L1 Constructs, IAM, and Cross-Stack Props: "GlueStack"
 * ==========================================================================
 *
 * CONCEPTS:
 *   - L1 vs L2 constructs → L2 (`s3.Bucket`, `iam.Role`) = high-level, opinionated
 *     defaults + helper methods. L1 (`CfnXxx`) = 1:1 mirror of a CloudFormation
 *     resource — every property maps directly to the CFN docs. Glue has NO
 *     stable L2 in CDK v2, so CfnDatabase / CfnJob / CfnCrawler are what you use.
 *   - Cross-stack props → pass RESOURCE OBJECTS (e.g. `s3.Bucket`), not ARN
 *     strings, so CDK can auto-resolve references AND you can call `.grantRead()`
 *     etc. on them inside this stack.
 *   - iam.Role + ServicePrincipal → "who can assume this role". Glue assumes
 *     this role at runtime to read/write your buckets and write to the catalog.
 *   - bucket.grantRead() / grantReadWrite() → CDK writes the correct least-
 *     privilege IAM policy statements for you (no hand-written ARNs).
 *
 * REAL-WORLD REFERENCE:
 *   This mirrors lib/glue-stack.ts in aws-etl-pipeline-cdk — "Stack 2", which
 *   depends on the 3 buckets created by StorageStack (Exercise 01).
 *
 * RUN:
 *   cd typescript/cdk && npm install   (if you haven't already)
 *   npx tsx exercises/02_glue_stack.ts
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as glue from 'aws-cdk-lib/aws-glue';
import { Template } from 'aws-cdk-lib/assertions';

// ---- EXAMPLE (for reference) ----
//
// A standalone L1 Glue database — no IAM, no job, just to show the CfnXxx shape.
// Notice: `databaseInput` is a nested object, exactly like the CloudFormation
// "Properties" block for AWS::Glue::Database would look in a template.
class CatalogStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new glue.CfnDatabase(this, 'ExampleDatabase', {
      catalogId: this.account, // every Glue catalog resource needs the AWS account ID
      databaseInput: {
        name:        'example_db',
        description: 'Just an example for Exercise 02',
      },
    });
  }
}

// ---- TASK 1: Props that take resources from Exercise 01's StorageStack ----
//
// interface GlueStackProps extends cdk.StackProps {
//   rawBucket:       s3.Bucket;
//   processedBucket: s3.Bucket;
//   scriptsBucket:   s3.Bucket;
// }

// YOUR CODE HERE

interface GlueStackProps extends cdk.StackProps {
  // ...
}

// ---- TASK 2: GlueStack ----
//
// class GlueStack extends cdk.Stack {
//   readonly jobName:      string;
//   readonly crawlerName:  string;
//   readonly databaseName: string;
//
//   constructor(scope, id, props: GlueStackProps) { ... }
// }
//
// Inside the constructor, build (in this order):
//
//  a) this.databaseName = 'practice_db'
//     new glue.CfnDatabase(...) using databaseInput.name = this.databaseName
//
//  b) IAM role for the Glue job:
//     new iam.Role(this, 'GlueJobRole', {
//       assumedBy: new iam.ServicePrincipal('glue.amazonaws.com'),
//       managedPolicies: [iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSGlueServiceRole')],
//     })
//     then: props.rawBucket.grantRead(role)
//           props.processedBucket.grantReadWrite(role)
//
//  c) Glue ETL Job (L1 — glue.CfnJob):
//     new glue.CfnJob(this, 'TransformJob', {
//       name: 'practice-transform-job',
//       role: <the role's roleArn>,
//       command: { name: 'glueetl', pythonVersion: '3', scriptLocation: `s3://${props.scriptsBucket.bucketName}/jobs/transform.py` },
//       glueVersion: '4.0',
//       workerType: 'G.1X',
//       numberOfWorkers: 2,
//     })
//     this.jobName = job.name!   (note the `!` — CfnJob.name is optional in the
//                                  type system even though we always set it)
//
//  d) IAM role + Crawler that scans processedBucket:
//     new iam.Role(this, 'GlueCrawlerRole', { assumedBy: ServicePrincipal('glue.amazonaws.com'), managedPolicies: [...] })
//     props.processedBucket.grantRead(crawlerRole)
//     new glue.CfnCrawler(this, 'ProcessedCrawler', {
//       name: 'practice-crawler',
//       role: crawlerRole.roleArn,
//       databaseName: this.databaseName,
//       targets: { s3Targets: [{ path: `s3://${props.processedBucket.bucketName}/processed/` }] },
//       schemaChangePolicy: { updateBehavior: 'LOG', deleteBehavior: 'LOG' },
//     })
//     this.crawlerName = crawler.name!

// YOUR CODE HERE

class GlueStack extends cdk.Stack {
  // readonly jobName: string;
  // readonly crawlerName: string;
  // readonly databaseName: string;

  constructor(scope: Construct, id: string, props: GlueStackProps) {
    super(scope, id, props);

    // ...
  }
}

// ---- TASK 3: Wire it up (this is the "app.ts" pattern in miniature) ----
//
// Create 3 buckets directly here (a stand-in for Exercise 01's StorageStack
// outputs), then instantiate GlueStack passing them as props.

// YOUR CODE HERE
// const app = new cdk.App();
// const helperStack = new cdk.Stack(app, 'Buckets');
// const rawBucket       = new s3.Bucket(helperStack, 'Raw');
// const processedBucket = new s3.Bucket(helperStack, 'Processed');
// const scriptsBucket   = new s3.Bucket(helperStack, 'Scripts');
// const glueStack = new GlueStack(app, 'TestGlue', { rawBucket, processedBucket, scriptsBucket });

// ---- TESTS ---- (uncomment after implementing)

/*
const template = Template.fromStack(glueStack);

template.resourceCountIs('AWS::Glue::Database', 1);
template.resourceCountIs('AWS::Glue::Job', 1);
template.resourceCountIs('AWS::Glue::Crawler', 1);

// The job's IAM role trust policy must allow glue.amazonaws.com to assume it
template.hasResourceProperties('AWS::IAM::Role', {
  AssumeRolePolicyDocument: {
    Statement: [
      { Action: 'sts:AssumeRole', Principal: { Service: 'glue.amazonaws.com' } },
    ],
  },
});

template.hasResourceProperties('AWS::Glue::Job', {
  Command: { Name: 'glueetl', PythonVersion: '3' },
  GlueVersion: '4.0',
});

console.log('✓ 02_glue_stack — all tests passed');
*/

void CatalogStack; // suppress unused-variable lint for the EXAMPLE class
